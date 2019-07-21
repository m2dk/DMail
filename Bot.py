#!/usr/bin/env python3
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, InlineQueryHandler, CommandHandler 
from telegram.ext import MessageHandler, Filters, ConversationHandler, RegexHandler, CallbackQueryHandler
from telegram.ext import ChosenInlineResultHandler
import requests
import re
import logging
import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger=logging.getLogger(__name__)

def start(bot, update):
	chat_id = update.message.chat_id
	time = update.message.date
	if(int(time.strftime("%H")) > 6 and int(time.strftime("%H")) < 12):
   		bot.send_message(chat_id=chat_id, text='¡Buenos días!, bienvenido a DMail creado por M2DK.')
	elif(int(time.strftime("%H")) > 12 and int(time.strftime("%H")) < 19):
		bot.send_message(chat_id=chat_id, text='¡Buenas tardes!, bienvenido a DMail creado por M2DK.')
	else:
		bot.send_message(chat_id=chat_id, text='¡Buenas noches!, bienvenido a DMail creado por M2DK.')
	reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("Si",callback_data="conection"),telegram.InlineKeyboardButton("No",callback_data="conectioff")]])
	bot.send_message(chat_id=chat_id, text ="¿Quieres usar nuestros servicios?", reply_markup=reply_markup)

def main():
    updater = Updater('983311490:AAHV5drXxXlgIqqGb0R0Z5tLA3BW2lxOdls')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()