from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Update
import requests
import re
import logging
from advertisement_db import Advertisement, AdvertisementDB
from users_db import UserFlags, UsersDB

API_KEY = open('secret.txt', 'r').read().strip()

base_actions = ['anuncis', 'dog', 'cercar', 'ajuda', 'afegir', 'borrar']
ad_actions = ['contactar', 'feedback']
mockup_advertisements_db = None
mockup_users_db = None

# region Helper Methods

# Simple function that helps me get a debug message on the bots console
def basic_callback_debug(update: Update, context: CallbackQuery, command_name: str):
    print('command ' + command_name + ' received from chat with id ' +
          str(update.message.chat_id) + ' and name ' +
          str(update.message.from_user.username))

# Response for an unimplemented feature
def unimplemented_function(update):
    update.message.reply_text("This feature hasn't been implemented yet.")

def add_dispatcher_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler(base_actions[0], get_ads_handler))
    # dispatcher.add_handler(CommandHandler(base_actions[2], search_handler))
    dispatcher.add_handler(CommandHandler(base_actions[4], new_ad_handler))
    dispatcher.add_handler(CommandHandler(base_actions[5], remove_ad_handler))
    dispatcher.add_handler(CommandHandler(base_actions[3], help_handler))
    dispatcher.add_handler(CommandHandler('placeholder', placeholder_handler))
    dispatcher.add_handler(CallbackQueryHandler(button_pressed_handler))
    dispatcher.add_handler(MessageHandler(
        Filters.text, message_received_handler))


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

# endregion

# region Commands

# START Command - executed when the conversation starts
def start(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name='start')
    mockup_users_db.add(update.message.from_user.id)

    kb_buttons = [[KeyboardButton('/' + base_actions[0]), KeyboardButton('/' + base_actions[4])],
                  [KeyboardButton('/' + base_actions[5]), KeyboardButton('/' + base_actions[3])]]
    kb_markup = ReplyKeyboardMarkup(kb_buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text='Selecciona una opció:',
                             reply_markup=kb_markup)

# ADS Command - return a list of ads of interest to the user
def get_ads_handler(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name=base_actions[0])
    # Get a list of relevant ads for the user and generete messages for it
    ads = mockup_advertisements_db.get_all()
    for a in ads:
        send_ad(update, context, a)

def send_ad(update, context, advertisement):
    ad_buttons = [InlineKeyboardButton(ad_actions[0], callback_data=ad_actions[0]),
                  InlineKeyboardButton(ad_actions[1], callback_data=ad_actions[1])]

    reply_markup = InlineKeyboardMarkup(build_menu(ad_buttons, n_cols=2))
    message = '[id:' + str(advertisement.id) + '] ' + advertisement.message
    context.bot.send_message(update.message.chat_id,
                             text=message, reply_markup=reply_markup)

def new_ad_handler(update: Update, context: CallbackQuery):
    mockup_users_db.set_flag(update.message.from_user.id, UserFlags.FLAG_ADD)
    update.message.reply_text( "Please, write the message of your advertisement.")

def add_new_ad(update):
    mockup_advertisements_db.add(update.message.text)
    update.message.reply_text("New add created.")

def remove_ad_handler(update: Update, context: CallbackQuery):
    mockup_users_db.set_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)
    update.message.reply_text( "Please, write the advertisement id to be removed.")

def remove_selected_ad(update):
    mockup_advertisements_db.remove(update.message.text)
    update.message.reply_text("Advertisement removed.")

def message_received_handler(update: Update, context: CallbackQuery):
    if (mockup_users_db.get_flag(update.message.from_user.id, UserFlags.FLAG_ADD)):
        add_new_ad(update)
    elif (mockup_users_db.get_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)):
        remove_selected_ad(update)
    mockup_users_db.unset_flag(update.message.from_user.id, UserFlags.FLAG_ADD)
    mockup_users_db.unset_flag(update.message.from_user.id, UserFlags.FLAG_REMOVE)

# SEARCH Command - asks for an input text and returns a list of shops who meet the
# desired searching criteria
# [currently unimplemented]
def search_handler(update, context):
    basic_callback_debug(update, context, command_name=base_actions[2])
    placeholder_handler(update, context)

# HELP Command - returns a pretty-printed list of commands and useful information
# [currently unimplemented]
def help_handler(update: Update, context: CallbackQuery):
    basic_callback_debug(update, context, command_name=base_actions[3])
    placeholder_handler(update, context)

# 
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
    global mockup_advertisements_db
    global mockup_users_db
    mockup_advertisements_db = AdvertisementDB('advertisement_test.db')
    mockup_users_db = UsersDB("users_test.db")

    updater = Updater(str(API_KEY),
                      use_context=True)
    dispatcher = updater.dispatcher
    add_dispatcher_handlers(dispatcher)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s' +
                        ' - %(message)s', level=logging.INFO)

    updater.start_polling()
    updater.idle()

# endregion


if __name__ == '__main__':
    main()
