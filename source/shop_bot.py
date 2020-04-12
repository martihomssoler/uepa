#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_utils import *

API_KEY = open('../data/shop_secret.txt', 'r').read().strip()

shop_actions: List[List[Union[str, Callable]]] = None
mockup_advertisements_db = None
mockup_users_db = None
mockup_shops_db = None

LOCATION, CONTACT, NAME, DESCRIPTION, CATEGORY = range(5)
AD_DESCRIPTION = range(1)

CATEGORY_LIST = ['Serveis generals', 'Alimentació', 'Hosteleria', 'Roba i Complements', 
                 'Llar', 'Salut i benestar', 'Altres', 'Oci i Cultura']

# region Helper Methods

# adds the callback handlers of the bot # this is actually the logic and brains 
# of the bot without handlers it cannot answer to any action done by the user
def add_dispatcher_handlers(dispatcher):
    # this handler should be for the inline ad buttons
    dispatcher.add_handler(CallbackQueryHandler(button_pressed_handler))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(' + get_actions() + 
                       ')$'), message_received_handler))

    # Add conversation handler with the states LOCATION, CONTACT, NAME, DESCRIPTION, CATEGORY
    login_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LOCATION: [MessageHandler(Filters.location, set_location_handler_state)],
            CONTACT: [MessageHandler(Filters.contact, set_contact_handler_state)],
            NAME: [MessageHandler(Filters.text, set_name_handler_state)],
            DESCRIPTION: [MessageHandler(Filters.text, set_description_handler_state)],
            CATEGORY: [MessageHandler(Filters.regex('^(' + get_categories(CATEGORY_LIST) + 
                       '|Finalitzar)$'), set_category_handler_state)]
        },

        fallbacks=[CommandHandler('cancel', cancel_handler_state)]
    )
    dispatcher.add_handler(login_conversation_handler)

    # Add conversation handler with the states AD_DESCRIPTION
    ad_creation_conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(' + emojize(':heavy_plus_sign: Afegir Anunci', 
                      use_aliases=True) + ')$'), ad_creation_handler_state)],

        states={
            AD_DESCRIPTION: [MessageHandler(Filters.text, add_description_handler_state)]
        },

        fallbacks=[CommandHandler('cancel', cancel_handler_state)]
    )
    dispatcher.add_handler(ad_creation_conversation_handler)

def get_actions():
    actions = []
    modified_action = [emojize(':x: Borrar', use_aliases=True), 
                       emojize(':question: Ajuda', use_aliases=True)]
    for action in modified_action:
        actions.append(action)
    return '|'.join(actions)

def get_categories(cat_list):
    return '|'.join(cat_list)

def set_main_menu(update: Update, context: CallbackQuery):
    kb_buttons = []
    for [action, _] in shop_actions:
        kb_buttons.append(KeyboardButton(action)) 
    kb_buttons = build_menu(kb_buttons, 2)

    kb_markup = ReplyKeyboardMarkup(kb_buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text='Selecciona una opció:',
                             reply_markup=kb_markup)

# endregion

# region Commands

# START Command - executed when the conversation starts
def start(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='start')
    return start_handler_state(update, context)

# REMOVE Command - asks for the desired advertisement id to be removed
def remove_ad_handler(update: Update, context: CallbackQuery):
    mockup_users_db.set_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)
    update.message.reply_text(
        "Si us plau, escriviu l'identificador de l'anunci que voleu eliminar.")

# get the content of the current message as the advertisement ID to be removed
def remove_selected_ad(update: Update, context: CallbackQuery):
    mockup_advertisements_db.remove(update.message.text)
    # TODO check if an advertisement was indeed removed
    update.message.reply_text("Anunci eliminat!")

# MESSAGE RECEIVED - handler executed whenever a TEXT message is received from the user
def message_received_handler(update: Update, context: CallbackQuery):
    for [action, handler] in shop_actions:
        if (update.message.text == action):
            handler(update, context)
            return

    # if the bot was waiting to receive the content of a new advertisement
    # then it will use the message content to create a new ad
    if (mockup_users_db.get_flag(update.message.from_user.id, UserFlags.FLAG_ADD)):
        add_description_handler_state(update, context)
        # the user has sent a message and the flags have to be unset
        unset_all_flags(update.message.from_user.id)

    # if the bot was waiting to receive the advertisement id of the advertisement to be removed
    # then it will use the message content as the ID to remove the ad
    elif (mockup_users_db.get_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)):
        remove_selected_ad(update, context)
        # the user has sent a message and the flags have to be unset
        unset_all_flags(update.message.from_user.id)

def unset_all_flags(user_id: int):
    mockup_users_db.unset_flag(user_id, UserFlags.FLAG_ADD)
    mockup_users_db.unset_flag(user_id, UserFlags.FLAG_REMOVE)

# HELP Command - returns a pretty-printed list of commands and useful information
# [currently unimplemented]
def help_handler(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='help')
    placeholder_handler(update, context)

# ADVERTISEMENT INLINE BUTTONS - handler executed whenever an inlined button from an advertisement 
# is interacted with
def button_pressed_handler(update: Update, context: CallbackQuery):
    query: CallbackQuery = update.callback_query
    print('user interacted with ' + query.message.text + ' and pressed ' + query.data +
          ' button pressed by user ' + str(query.from_user.username))

# PLACEHOLDER Command - unimplemented function
def placeholder_handler(update: Update, context: CallbackQuery):
    print("Unimplemented placeholder")
    unimplemented_function(update)

# endregion

# region Login Conversation States

def start_handler_state(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='start')
    print('user id: ' + str(update.message.from_user.id))
    mockup_users_db.add(update.message.from_user.id)
    kb_markup = ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text=emojize('''Si us plau, envia la localització on es troba la seva botiga.\n
Per compartir ubicació, clica a l' imatge del clip :paperclip: a la dreta de la barra de xat.\n
Una vegada dins, seleccione Ubicació :pushpin: per compartir-la! ''', use_aliases=True),
                             reply_markup=kb_markup)
    return LOCATION

def set_location_handler_state(update: Update, context: CallbackQuery):
    user = update.message.from_user
    user_location = update.message.location
    logging.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                 user_location.longitude)
    mockup_shops_db.add(user.id, user_location.longitude, user_location.latitude)
    update.message.reply_text(emojize('''Si us plau, envïi'ns els seu contacte.\n
Per compartir el contacte, fes clic als tres punts (...) de la part superior dreta de la pantalla.\n
A continuació, clica en "Compartir contacte" :iphone: ''', use_aliases=True))
    return CONTACT

def set_contact_handler_state(update: Update, context: CallbackQuery):
    user = update.message.from_user
    phone_number = update.message.contact.phone_number
    logging.info("Phone number of %s: %s", user.first_name, phone_number)
    mockup_shops_db.set_phone_number(user.id, phone_number)
    update.message.reply_text("Diga'ns quin nom te la seva botiga.")
    return NAME

def set_name_handler_state(update: Update, context: CallbackQuery):
    user = update.message.from_user
    shop_name = update.message.text
    logging.info("The name of %s's shop is %s.", user.first_name, shop_name)
    mockup_shops_db.set_name(user.id, shop_name)
    update.message.reply_text("Descriu la seva botiga.")
    return DESCRIPTION

def set_description_handler_state(update: Update, context: CallbackQuery):
    user = update.message.from_user
    description = update.message.text
    logging.info("The description of %s's shop is: %s.", user.first_name, description)
    mockup_shops_db.set_description(user.id, description)

    kb_buttons = []
    for cat in CATEGORY_LIST:
        kb_buttons.append(KeyboardButton(cat))
    kb_buttons.append(KeyboardButton('Finalitzar'))
    kb_buttons = build_menu(kb_buttons, 2)
    kb_markup = ReplyKeyboardMarkup(kb_buttons)
    
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text="Selecciona les categories que mes escauen al teu negoci.",
                             reply_markup=kb_markup)
    return CATEGORY

def set_category_handler_state(update: Update, context: CallbackQuery):
    user = update.message.from_user
    category = update.message.text

    if (category == 'Finalitzar'):
        kb_markup = ReplyKeyboardRemove()
        context.bot.send_message(chat_id=update.message.chat_id, 
                                text="Ja tenim tot el que necessitem. Benvingut a UEPA!",
                                reply_markup=kb_markup)
        set_main_menu(update, context)
        return ConversationHandler.END
    
    category_list = mockup_shops_db.get(user.id).categories
    if (category_list != None and category in category_list):
        if (category + ', ' in category_list):
            category_list = category_list.replace(category + ', ', '')
        elif (', ' + category in category_list):
            category_list = category_list.replace(', ' + category, '')
        else:
            category_list = category_list.replace(category, '')
        mockup_shops_db.set_categories(user.id, category_list)
    else:
        mockup_shops_db.add_category(user.id, category)
    
    update.message.reply_text("Categories: " + mockup_shops_db.get(user.id).categories)
    return CATEGORY

def cancel_handler_state(update: Update, context: CallbackQuery):
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.first_name)
    set_main_menu(update, context)
    # TODO erase the info in the DB
    return ConversationHandler.END

# endregion

# ADD Command - asks for the desired advertisement content message to be added
def ad_creation_handler_state(update: Update, context: CallbackQuery):
    mockup_users_db.set_flag(update.message.from_user.id, UserFlags.FLAG_ADD)
    update.message.reply_text(
        "Si us plau, escriviu el contingut del nou anunci que voleu crear.")
    return AD_DESCRIPTION

# get the content of the current message as the advertisement message to be created
def add_description_handler_state(update: Update, context: CallbackQuery):
    mockup_advertisements_db.add(update.message.from_user.id, update.message.text)
    # TODO check if an advertisement was indeed created
    update.message.reply_text("Nou anunci creat!")
    return ConversationHandler.END

# region Ad Creation Conversation States

# endregion

# region Main Method

def main():
    # initialize the databases
    # in case the file already exists it will load the file
    # in case the file does not exists it will create an empty table
    global mockup_advertisements_db
    global mockup_users_db
    global mockup_shops_db
    mockup_advertisements_db = AdvertisementDB('../data/advertisement_test.db')
    mockup_users_db = UsersDB("../data/users_test.db")
    mockup_shops_db = ShopDB("../data/shop_test.db")

    global shop_actions
    shop_actions = [[emojize(':heavy_plus_sign: Afegir Anunci', use_aliases=True), ad_creation_handler_state], 
                    [emojize(':x: Borrar Anunci', use_aliases=True), remove_ad_handler], 
                    [emojize(':bulb: Ajuda', use_aliases=True), help_handler],
                    [emojize(':newspaper: Què es cou', use_aliases=True), start]]
    
    # connect to the API with the key inside the secret.txt file
    updater = Updater(str(API_KEY),
                      use_context=True)
    dispatcher = updater.dispatcher
    add_dispatcher_handlers(dispatcher)

    # add a debugging/logging configuration to get a more granulated and
    # useful exception dump
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s' +
                        ' - %(message)s', level=logging.INFO)

    # start the application
    updater.start_polling()
    updater.idle()

# endregion

if __name__ == '__main__':
    main()
