from bot_utils import *

API_KEY = open('../data/client_secret.txt', 'r').read().strip()

client_actions: List[List[Union[str, Callable]]] = None
ad_actions = ['contactar', 'feedback']
mockup_advertisements_db = None
mockup_users_db = None

# region Helper Methods

# adds the callback handlers of the bot # this is actually the logic and brains 
# of the bot without handlers it cannot answer to any action done by the user
def add_dispatcher_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    # this handler should be for the inline ad buttons
    dispatcher.add_handler(CallbackQueryHandler(button_pressed_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_received_handler))

# endregion

# region Commands

# START Command - executed when the conversation starts
def start(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='start')
    mockup_users_db.add(update.message.from_user.id)

    kb_buttons = []
    for [action, _] in client_actions:
        kb_buttons.append(KeyboardButton(action)) 
    kb_buttons = build_menu(kb_buttons, 2)

    kb_markup = ReplyKeyboardMarkup(kb_buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text='Selecciona una opció:',
                             reply_markup=kb_markup)

# ADS Command - return a list of ads of interest to the user
def get_ads_handler(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='get ads')
    # Get a list of relevant ads for the user and generete messages for it
    ads = mockup_advertisements_db.get_all()
    if (ads == []):
        update.message.reply_text("Maulauradament no hem pogut trobar cap anunci. " + 
            "Contacta amb el teu comerç més proper i anima’l a usar <b>Uepa!</b>",
            parse_mode=ParseMode.HTML)
    else:
        for a in ads:
            send_ad(update, context, a)

# given an advertisement it will send the advertisement message with its own
# inline keyboard buttons
def send_ad(update, context, advertisement):
    ad_buttons = [InlineKeyboardButton(ad_actions[0], callback_data=ad_actions[0]),
                  InlineKeyboardButton(ad_actions[1], callback_data=ad_actions[1])]

    reply_markup = InlineKeyboardMarkup(build_menu(ad_buttons, n_cols=2))
    message = '[id:' + str(advertisement.id) + '] ' + advertisement.message
    context.bot.send_message(update.message.chat_id,
                             text=message, reply_markup=reply_markup)

# MESSAGE RECEIVED - handler executed whenever a TEXT message is received from the user
def message_received_handler(update: Update, context: CallbackQuery):    
    for [action, handler] in client_actions:
        if (update.message.text == action):
            handler(update, context)
            return

# SEARCH Command - asks for an input text and returns a list of shops who meet the
# desired searching criteria
# [currently unimplemented]
def search_handler(update, context):
    basic_callback_debug(update, context, command_name='search')
    placeholder_handler(update, context)

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

# region Main Method

def main():
    # initialize the databases
    # in case the file already exists it will load the file
    # in case the file does not exists it will create an empty table
    global mockup_advertisements_db
    global mockup_users_db
    mockup_advertisements_db = AdvertisementDB('../data/advertisement_test.db')
    mockup_users_db = UsersDB("../data/users_test.db")

    global client_actions
    client_actions = [[emojize(':newspaper: Anuncis', use_aliases=True), get_ads_handler], 
                    [emojize(':mag: Cercar', use_aliases=True), search_handler], 
                    [emojize(':question: Ajuda', use_aliases=True), help_handler],
                    [emojize(':star2: Start', use_aliases=True), start]]

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
