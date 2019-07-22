#!/usr/bin/env python3
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram.ext import ChosenInlineResultHandler
import requests
import re
import logging
import datetime
import re
from sys import exit
from imapclient import IMAPClient, SEEN
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib, ssl
from email import encoders

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger=logging.getLogger(__name__)

def start(bot, update):
	chat_id = update.message.chat_id
	time = update.message.date
	if(int(time.strftime("%H")) > 6 and int(time.strftime("%H")) < 12):
		bot.send_message(chat_id=chat_id, text='¡Buenos días!, bienvenido a DMail creado por M2DK.')
	elif(int(time.strftime("%H")) >= 12 and int(time.strftime("%H")) < 19):
		bot.send_message(chat_id=chat_id, text='¡Buenas tardes!, bienvenido a DMail creado por M2DK.')
	else:
		bot.send_message(chat_id=chat_id, text='¡Buenas noches!, bienvenido a DMail creado por M2DK.')

	keyboard= [[InlineKeyboardButton("Si",callback_data="conection"),InlineKeyboardButton("No",callback_data="conectioff")]]
	reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
	bot.send_message(chat_id=chat_id, text ="¿Quieres usar nuestros servicios?", reply_markup=reply_markup)
	

def button(bot, update):
	query = update.callback_query
	if (query.data=="conectioff"):
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Gracias por usar nuestro bot.")
	elif(query.data=="conection"):
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Para conectarse es necesario que nos indique su cuenta y contraseña")
		bot.send_message(chat_id=query.message.chat_id, text ="Cuenta:", reply_markup=telegram.ForceReply(True))
	elif(query.data=="revisar"):
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Veamos tus mensajes nuevos")
		with IMAPClient(HOST) as server:
			server.login(mail, contra)
			server.select_folder('INBOX', readonly=False)
			texto=''
			while(texto==''):
				try:
					server.idle()
					responses = server.idle_check(timeout=1)
					server.idle_done()
					recibido = server.search('UNSEEN')
					if(not(recibido == [])):
						bot.send_message(chat_id=query.message.chat_id,text="Mensajes nuevos:")
						print(recibido)
						for uid, message_data in server.fetch(recibido, 'RFC822').items():
							email_message = email.message_from_bytes(message_data[b'RFC822'])
							texto = "De:\n" + email_message.get('From') + "\nAsunto:\n" + email_message.get('Subject')
							bot.send_message(chat_id=query.message.chat_id, text=texto)
						if not SET_READ:
							server.remove_flags(recibido, [SEEN])
					else:
						bot.send_message(chat_id=query.message.chat_id,text="No hay nuevos mensajes")
						texto="1"
				except KeyboardInterrupt:
					server.logout()
					exit()
	elif(query.data=="enviar"):
		global aenviar
		aenviar = MIMEMultipart()
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Para enviar un mensaje es necesario que nos proporcione cierta información.\n En el caso de haber varios destinatarios separelos con una coma y un espacio (', ') unicamente")
		bot.send_message(chat_id=query.message.chat_id, text ="Destino:", reply_markup=telegram.ForceReply(True))


	


def comandos(bot,update):
	chat_id=update.message.chat_id
	respuesta=update.message.reply_to_message
	global mail
	global contra
	if (respuesta.text=="Cuenta:"):
		Email_Regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[gmail]+\.[com]*$")
		mail=update.message.text
		if (not Email_Regex.match(mail)):
			bot.send_message(chat_id=chat_id, text ="No tiene la estructura correcta (ejemplo@gmail.com)")
			bot.send_message(chat_id=chat_id, text ="Cuenta:", reply_markup=telegram.ForceReply(True))
		else:
			bot.send_message(chat_id=chat_id, text ="Contraseña:", reply_markup=telegram.ForceReply(True))
	elif(respuesta.text=="Contraseña:"):
		contra=update.message.text
		if (not(mail is None) and not(contra is None)): 
			with IMAPClient(HOST) as server:
				try:
					server.login(mail, contra)
					bot.send_message(chat_id=chat_id, text="Conectados") # Sticker deberia ir aqui
					keyboard= [[InlineKeyboardButton("Revisar",callback_data="revisar"),
					InlineKeyboardButton("Enviar",callback_data="enviar")]]
					reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
					bot.send_message(chat_id=chat_id, text ="¿Qué quieres hacer?", reply_markup=reply_markup)
				except:
					bot.send_message(chat_id=chat_id, text="No Conectados") #Sticker deberia ir aqui
	elif(respuesta.text=="Destino:"):
		Email_Regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
		mailes=update.message.text
		correos=mailes.split(', ')
		validador=False
		for correo in correos:
			if (not Email_Regex.match(correo)):
				bot.send_message(chat_id=chat_id, text ="No tiene la estructura correcta (ejemplo@gmail.com)")
				bot.send_message(chat_id=chat_id, text ="Destino:", reply_markup=telegram.ForceReply(True))
				validador=False
				break
			else:
				validador=True
		if (validador):
			aenviar["To"] = mailes
			bot.send_message(chat_id=chat_id, text ="Asunto:", reply_markup=telegram.ForceReply(True))
	elif(respuesta.text=="Asunto:"):
		aenviar["Subject"] = update.message.text
		bot.send_message(chat_id=chat_id, text ="Mensaje:", reply_markup=telegram.ForceReply(True))
	elif(respuesta.text=="Mensaje:"):
		aenviar.attach(MIMEText(update.message.text,"plain"))
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(HOST_E,465,context=context) as server:
			aenviar["From"] = mail
			server.login(mail, contra)
			server.sendmail(mail, aenviar['To'].split(","), aenviar.as_string())




HOST_E = 'smtp.gmail.com'
HOST='imap.gmail.com'
SET_READ=False

def main():
    updater=Updater('983311490:AAHV5drXxXlgIqqGb0R0Z5tLA3BW2lxOdls')
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text,comandos))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()