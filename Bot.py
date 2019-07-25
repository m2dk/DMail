#!/usr/bin/env python3
import telegram #Libreria general de telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup #Librerias particulares
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler #Librerias del bot1
from telegram.ext import MessageHandler, Filters, ConversationHandler, RegexHandler #Librerias del bot2
from telegram.ext import ChosenInlineResultHandler #Librerias del bot3
import re 
import logging
import datetime
import re
import urllib.request
from sys import exit
from imapclient import IMAPClient, SEEN #Librerias IMAP
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib, ssl #librerias SMTP
from email import encoders
import os
#Informacion para el log del bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger=logging.getLogger(__name__)


def start(bot, update): # Funcion de bienvenida y del comando Start del bot
	chat_id = update.message.chat_id #Id del chat
	time = update.message.date #Tiempo del mensaje
	if(int(time.strftime("%H")) > 6 and int(time.strftime("%H")) < 12): #Condicional para saludar de acuerdo a la hora
		bot.send_message(chat_id=chat_id, text='¡Buenos días!, bienvenido a DMail creado por M2DK.') #Envio de mensaje de bienvenida
	elif(int(time.strftime("%H")) >= 12 and int(time.strftime("%H")) < 19):
		bot.send_message(chat_id=chat_id, text='¡Buenas tardes!, bienvenido a DMail creado por M2DK.') #Envio de mensaje de bienvenida
	else:
		bot.send_message(chat_id=chat_id, text='¡Buenas noches!, bienvenido a DMail creado por M2DK.') #Envio de mensaje de bienvenida
	#Creacion del teclado de opciones 	
	keyboard= [[InlineKeyboardButton("Si",callback_data="conection"),InlineKeyboardButton("No",callback_data="conectioff")]]
	reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
	#Mensaje con el teclado
	bot.send_message(chat_id=chat_id, text ="¿Quieres usar nuestros servicios?", reply_markup=reply_markup)
	

def button(bot, update): #Función de manejo de botones
	query = update.callback_query #variable para almacenar el mensaje de llamada a los botones
	if (query.data=="conectioff"): #Mensaje de conexion en caso de no querer usar los servicios o desconexión
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Gracias por usar nuestro bot.") #editor del mensaje del boton para que no se presione más de una vez
	elif(query.data=="conection"): #Mensaje de conexion positiva
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Para conectarse es necesario que nos indique su cuenta y contraseña")#editor del mensaje del boton para que no se presione más de una vez
		#envio de mensaje con forcereply, para obligar al usuario a responder al mensaje de manera que se realice un formulario
		bot.send_message(chat_id=query.message.chat_id, text ="Cuenta:", reply_markup=telegram.ForceReply(True))
	elif(query.data=="revisar"): #Opcion de revisar mensaje
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, 
			text="Veamos tus mensajes nuevos") #Editor de mensaje
		with IMAPClient(HOST) as server: #Realiza la conexion de nuevo, proceso IMAP del laboratorio 1
			server.login(mail, contra) #Login con el mail y la contraseña ingresada por el usuario
			server.select_folder('INBOX', readonly=False) #Selecciona la carpeta
			texto='' #Variable para manejar el while
			while(texto==''): #While para manejar la recepción de mensajes
				try:
					server.idle() #Conexion Idle
					responses = server.idle_check(timeout=1) #Verificación
					server.idle_done() 
					recibido = server.search('UNSEEN') #Recibe los mensaje no vistos
					if(not(recibido == [])): #verifica que haya mensajes nuevos
						bot.send_message(chat_id=query.message.chat_id,text="Mensajes nuevos:") #mensaje de apertura
						for uid, message_data in server.fetch(recibido, 'RFC822').items(): #for de impresion
							email_message = email.message_from_bytes(message_data[b'RFC822'])
							texto = "De:\n" + email_message.get('From') + "\nAsunto:\n" + email_message.get('Subject')
							bot.send_message(chat_id=query.message.chat_id, text=texto) #Envio de mensaje
						if not SET_READ:
							server.remove_flags(recibido, [SEEN])
					else:
						bot.send_message(chat_id=query.message.chat_id,text="No hay nuevos mensajes")
						texto="1"
				except KeyboardInterrupt:
					server.logout()
					exit()
		#Generación del teclado para verificar si se quiere hacer algo mas
		rep(bot,query.message.chat_id)
	#opción de enviar mensaje
	elif(query.data=="enviar"):
		global aenviar #variable global de creacion de el objeto mensaje
		aenviar = MIMEMultipart()
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Para enviar un mensaje es necesario que nos proporcione cierta información.")
		bot.send_message(chat_id=query.message.chat_id,
			text="En el caso de haber varios destinatarios separelos con una coma y un espacio (', ') unicamente")
		#respuesta obligatoria para el destino del mensaje, luego de la explicación para enviar el mensaje a varios destinatarios
		bot.send_message(chat_id=query.message.chat_id, text ="Destino:", reply_markup=telegram.ForceReply(True))
	elif(query.data=="adjuntar"):
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Envienos el archivo a continuación")
		bot.send_message(chat_id=query.message.chat_id, text="Archivo:", reply_markup=telegram.ForceReply(True))
	elif(query.data=="noadjuntar"):
		bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
			text="Todo listo, procederemos a enviar el correo")
		envio(bot,query.message.chat_id)
			#repeticion final
		rep(bot,query.message.chat_id) 

	


def comandos(bot,update):
	chat_id=update.message.chat_id #id del chat
	respuesta=update.message.reply_to_message #mensaje de respuesta
	global mail #variable global de mail
	global contra #variable global de contraseña
	if (respuesta.text=="Cuenta:"): #Receptor de la cuenta a usar
		Email_Regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[gmail]+\.[com]*$") #Expresión regular del mensaje de respuesta
		mail=update.message.text #Texto del mensaje
		if (not Email_Regex.match(mail)): #if de condicion para validar que el correo cumpla con la expresión regular
			bot.send_message(chat_id=chat_id, text ="No tiene la estructura correcta (ejemplo@gmail.com)") #mensaje de error
			bot.send_message(chat_id=chat_id, text ="Cuenta:", reply_markup=telegram.ForceReply(True)) #mensaje de cuenta nuevo
		else:
			bot.send_message(chat_id=chat_id, text ="Contraseña:", reply_markup=telegram.ForceReply(True))
	elif(respuesta.text=="Contraseña:"): #Handler contraseña
		contra=update.message.text #texto de la contraseña
		if (not(mail is None) and not(contra is None)):  #valida que ambas tengan valores
			with IMAPClient(HOST) as server:
				try: #Primera conexion para verificar los datos
					server.login(mail, contra)
					bot.send_message(chat_id=chat_id, text="Conectados") # Sticker deberia ir aqui
					#menu de opciones una vez conectado
					keyboard= [[InlineKeyboardButton("Revisar",callback_data="revisar"),
					InlineKeyboardButton("Enviar",callback_data="enviar")]]
					reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
					bot.send_message(chat_id=chat_id, text ="¿Qué quieres hacer?", reply_markup=reply_markup)
				except: #mensaje de error
					bot.send_message(chat_id=chat_id, text="No Conectados") #Sticker deberia ir aqui
	elif(respuesta.text=="Destino:"): #Mensaje para la cuenta destino
		Email_Regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$") #Expresion regular para la cuenta a enviar
		mailes=update.message.text #mails a enviar
		correos=mailes.split(', ') #en caso de varias cuentas esto es necesario
		validador=False #variable de posible uso de los mails
		for correo in correos: #for para los correos de destinos y verificar su estructura
			if (not Email_Regex.match(correo)):
				bot.send_message(chat_id=chat_id, text ="No tiene la estructura correcta (ejemplo@gmail.com)")
				bot.send_message(chat_id=chat_id, text ="Destino:", reply_markup=telegram.ForceReply(True))
				validador=False
				break
			else:
				validador=True
		if (validador):
			aenviar["To"] = mailes #carga del destino
			bot.send_message(chat_id=chat_id, text ="Asunto:", reply_markup=telegram.ForceReply(True)) #envia el proximo paso
			#manejador paso del asunto
	elif(respuesta.text=="Asunto:"):
		aenviar["Subject"] = update.message.text #carga del asunto del mensaje (temporal hasta agregar archivos adjuntos)
		bot.send_message(chat_id=chat_id, text ="Mensaje:", reply_markup=telegram.ForceReply(True)) #mensaje para el cuerpo del correo
	elif(respuesta.text=="Mensaje:"): #manejador del cuerpo y el envio del mensaje
		aenviar.attach(MIMEText(update.message.text,"plain")) #agrega el mensaje
		keyboard = [[InlineKeyboardButton("Si",callback_data="adjuntar"),
		InlineKeyboardButton("No",callback_data="noadjuntar")]]
		reply_markup=InlineKeyboardMarkup(keyboard,one_time_keyboard=True)
		bot.send_message(chat_id=chat_id, text="¿Desea adjuntar algún archivo?", reply_markup= reply_markup)

def archivo(bot,update):#manejador de archivos funciona casi exactamente igual que el SMTP del laboratorio 2
	chat_id=update.message.chat_id #id del chat
	respuesta=update.message.reply_to_message #mensaje de respuesta
	if(respuesta.text=="Archivo:"):
		file_id = update.message.document.file_id
		file_name=update.message.document.file_name
		document = bot.getFile(file_id).file_path
		route = os.getcwd() + '/' + file_name
		urllib.request.urlretrieve(document,route)
		attachment = open(route, "rb")
		p = MIMEBase('application', 'octet-stream')
		p.set_payload((attachment).read())
		encoders.encode_base64(p)
		p.add_header('Content-Disposition', "attachment; filename= %s" %file_name)
		aenviar.attach(p)
		keyboard = [[InlineKeyboardButton("Si",callback_data="adjuntar"),
		InlineKeyboardButton("No",callback_data="noadjuntar")]]
		reply_markup=InlineKeyboardMarkup(keyboard,one_time_keyboard=True)
		bot.send_message(chat_id=chat_id, text="¿Desea adjuntar algún otro archivo?", reply_markup= reply_markup)


def rep(bot,chat): #funcion de repetición
	keyboard= [[InlineKeyboardButton("Revisar",callback_data="revisar"),
	InlineKeyboardButton("Enviar",callback_data="enviar"), InlineKeyboardButton("Nada", callback_data="conectioff")]]
	reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
	bot.send_message(chat_id=chat, text="¿Desea hacer algo más?", reply_markup=reply_markup)


def envio(bot,chat): #Funcion que envia el correo
	context = ssl.create_default_context() #contexto del mensaje
	with smtplib.SMTP_SSL(HOST_E,465,context=context) as server: #carga del mensaje
		aenviar["From"] = mail #carga del emisor
		server.login(mail, contra) #login al server
		try : #try catch para el envio del mensaje
			server.sendmail(mail, aenviar['To'].split(","), aenviar.as_string())#Envia el mensaje
			bot.send_message(chat_id=chat, text="Mensaje enviado") # mensaje de confirmación.
		except:
			bot.send_message(chat_id=chat, text= "Ocurrio un error al enviar el mensaje") #Manejador del mensaje


HOST_E = 'smtp.gmail.com'
HOST='imap.gmail.com'
SET_READ=False

def main():
    updater=Updater('983311490:AAHV5drXxXlgIqqGb0R0Z5tLA3BW2lxOdls')
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text,comandos))
    dp.add_handler(MessageHandler(Filters.document,archivo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



    