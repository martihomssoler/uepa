from bot_utils import *

API_KEY = open('shop_secret.txt', 'r').read().strip()

shop_actions = ['afegir', 'borrar', 'ajuda']
mockup_advertisements_db = None
mockup_users_db = None

# region Helper Methods

# adds the callback handlers of the bot # this is actually the logic and brains 
# of the bot without handlers it cannot answer to any action done by the user
def add_dispatcher_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler(shop_actions[0], new_ad_handler))
    dispatcher.add_handler(CommandHandler(shop_actions[1], remove_ad_handler))
    dispatcher.add_handler(CommandHandler(shop_actions[2], help_handler))
    dispatcher.add_handler(CommandHandler('placeholder', placeholder_handler))
    # this handler should be for the inline ad buttons
    dispatcher.add_handler(CallbackQueryHandler(button_pressed_handler))
    dispatcher.add_handler(MessageHandler(
        Filters.text, message_received_handler))

# endregion

# region Commands

# START Command - executed when the conversation starts
def start(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='start')
    mockup_users_db.add(update.message.from_user.id)

    kb_buttons = [[KeyboardButton('/' + shop_actions[0]), KeyboardButton('/' + shop_actions[1])],
                  [KeyboardButton('/start'), KeyboardButton('/' + shop_actions[2])]]
    kb_markup = ReplyKeyboardMarkup(kb_buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text='Selecciona una opció:',
                             reply_markup=kb_markup)

# ADD Command - asks for the desired advertisement content message to be added
def new_ad_handler(update: Update, context: CallbackQuery):
    mockup_users_db.set_flag(update.message.from_user.id, UserFlags.FLAG_ADD)
    update.message.reply_text( "Please, write the message of your advertisement.")

# get the content of the current message as the advertisement message to be created
def add_new_ad(update):
    mockup_advertisements_db.add(update.message.text)
    # TODO check if an advertisement was indeed created
    update.message.reply_text("New add created.")

# REMOVE Command - asks for the desired advertisement id to be removed
def remove_ad_handler(update: Update, context: CallbackQuery):
    mockup_users_db.set_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)
    update.message.reply_text( "Please, write the advertisement id to be removed.")

# get the content of the current message as the advertisement ID to be removed
def remove_selected_ad(update):
    mockup_advertisements_db.remove(update.message.text)
    # TODO check if an advertisement was indeed removed
    update.message.reply_text("Advertisement removed.")

# MESSAGE RECEIVED - handler executed whenever a TEXT message is received from the user
def message_received_handler(update: Update, context: CallbackQuery):
    # if the bot was waiting to receive the content of a new advertisement
    # then it will use the message content to create a new ad
    if (mockup_users_db.get_flag(update.message.from_user.id, UserFlags.FLAG_ADD)):
        add_new_ad(update)
        # the user has sent a message and the flags have to be unset
        unset_all_flags(update.message.from_user.id)

    # if the bot was waiting to receive the advertisement id of the advertisement to be removed
    # then it will use the message content as the ID to remove the ad
    elif (mockup_users_db.get_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)):
        remove_selected_ad(update)
        # the user has sent a message and the flags have to be unset
        unset_all_flags(update.message.from_user.id)
    

def unset_all_flags(user_id: int):
    mockup_users_db.unset_flag(user_id, UserFlags.FLAG_ADD)
    mockup_users_db.unset_flag(user_id, UserFlags.FLAG_REMOVE)

# HELP Command - returns a pretty-printed list of commands and useful information
# [currently unimplemented]
def help_handler(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name=shop_actions[2])
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

# region Main Method

def main():
    # initialize the databases
    # in case the file already exists it will load the file
    # in case the file does not exists it will create an empty table
    global mockup_advertisements_db
    global mockup_users_db
    mockup_advertisements_db = AdvertisementDB('advertisement_test.db')
    mockup_users_db = UsersDB("users_test.db")

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