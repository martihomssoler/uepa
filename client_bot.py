from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import requests
import re
import logging
from advertisement_db import Advertisement
from advertisement_db import AdvertisementDB

API_KEY = open('secret.txt', 'r').read().strip()

base_actions = ['anuncis','dog','cercar','ajuda', 'afegir', 'borrar']
ad_actions = ['contactar','feedback']
mockup_ad = Advertisement("this is a mockup advertisement", 1, 1)
mockup_db = None
is_writing_ad = False
is_removing_ad = False

#region Helper Methods

def basic_callback_debug(update, context, command_name):
    print('command ' + command_name + ' received from chat with id ' + 
          str(update.message.chat_id) + ' and name ' + 
          update.message.from_user.username)

def unimplemented_function(update):
    update.message.reply_text("This feature hasn't been implemented yet.")

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def add_dispatcher_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler(base_actions[0], get_ads_handler))
    # dispatcher.add_handler(CommandHandler(base_actions[1], dog_handler))
    # dispatcher.add_handler(CommandHandler(base_actions[2], search_handler))
    dispatcher.add_handler(CommandHandler(base_actions[4], new_ad_handler))
    dispatcher.add_handler(CommandHandler(base_actions[5], remove_ad_handler))
    dispatcher.add_handler(CommandHandler(base_actions[3], help_handler))
    dispatcher.add_handler(CommandHandler('placeholder', placeholder_handler))
    dispatcher.add_handler(CallbackQueryHandler(button_pressed_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_received_handler))

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

#endregion

#region Commands

# START Command - executed when the conversation starts
def start(update, context):
    basic_callback_debug(update, context, command_name='start')
    global mockup_db
    mockup_db = AdvertisementDB('test.db')

    kb_buttons = [[KeyboardButton('/' + base_actions[0]), KeyboardButton('/' + base_actions[4])],
                [KeyboardButton('/' + base_actions[5]), KeyboardButton('/' + base_actions[3])]]
    kb_markup = ReplyKeyboardMarkup(kb_buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text='Selecciona una opció:',
                             reply_markup=kb_markup)

# ADS Command - return a list of ads of interest to the user
def get_ads_handler(update, context):
    basic_callback_debug(update, context, command_name=base_actions[0])
    # Get a list of relevant ads for the user and generete messages for it
    ads = mockup_db.get_all()
    for a in ads:
        send_ad(update, context, a)

def send_ad(update, context, advertisement):
    ad_buttons = [InlineKeyboardButton(ad_actions[0], callback_data=ad_actions[0]),
                   InlineKeyboardButton(ad_actions[1], callback_data=ad_actions[1])]
    
    reply_markup = InlineKeyboardMarkup(build_menu(ad_buttons, n_cols=2))
    message = '[id:' + str(advertisement.id) + '] ' + advertisement.message
    context.bot.send_message(update.message.chat_id, text=message, reply_markup=reply_markup)

def new_ad_handler(update, context):
    global is_writing_message
    is_writing_message = True
    update.message.reply_text("Please, write the message of your advertisement.")

def add_new_ad(text):
    mockup_db.add(text)

def remove_ad_handler(update, context):
    global is_removing_ad
    is_removing_ad = True

def remove_selected_ad(identifier):
    mockup_db.remove(identifier)

def message_received_handler(update, context):
    global is_writing_ad
    global is_removing_ad
    if (is_writing_ad):
        add_new_ad(update.message.text)
    elif (is_removing_ad):
        remove_selected_ad(update.message.text)
    is_writing_ad = False
    is_removing_ad = False

# DOG Command - return a random image of a dog [PLACEHOLDER]
def dog_handler(update, context):
    basic_callback_debug(update, context, command_name=base_actions[1])
    
    photo_url = get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=photo_url)

# SEARCH Command - asks for an input text and returns a list of shops who meet the
# desired searching criteria
def search_handler(update, context):
    basic_callback_debug(update, context, command_name=base_actions[2])
    placeholder_handler(update, context)

# HELP Command - returns a pretty-printed list of commands and useful information
def help_handler(update, context):
    basic_callback_debug(update, context, command_name=base_actions[3])
    placeholder_handler(update, context)

def button_pressed_handler(update, context):
    query: CallbackQuery = update.callback_query
    print('user interacted with ' + query.message.text + ' and pressed ' + query.data +
          ' button pressed by user ' + query.from_user.username)

# PLACEHOLDER Command - unimplemented function
def placeholder_handler(update, context):
    print("Unimplemented placeholder")
    unimplemented_function(update)

#endregion

#region Main Method
def main():
    updater = Updater(str(API_KEY), 
                      use_context=True)
    dispatcher = updater.dispatcher
    add_dispatcher_handlers(dispatcher)
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s' + 
                        ' - %(message)s', level=logging.INFO)
    
    updater.start_polling()
    updater.idle()

#endregion

if __name__ == '__main__':
    main()