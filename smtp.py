from sys import exit
from imapclient import IMAPClient, SEEN
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib , ssl
from email import encoders
import configparser
import os


config = configparser.ConfigParser()
config.read("client.ini")

PORT = config ['server']['port']
SMTP_SERVER = config ['server']['smtp_server']
#RECEIVER_EMAIL = config ['receiver']['receiver_email']
SENDER_EMAIL = config ['account']['mailaddr']
SENDER_PASS = config ['account']['password']
MSG = MIMEMultipart()
MSG["Subject"] = config ['receiver']['subject']
MSG["To"] = config ['receiver']['receiver_email']
MESSAGE = MIMEText(config ['receiver']['message'])
#Apertura de archivos /home/lo/Downloads/archiv.txt /home/lo/Downloads/pruebaimg.jpg 
filename = config ['file']['name']
route = os.getcwd()+'/'+filename
attachment = open (route, "rb")
#MIMEbase
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" %filename)
MSG.attach(MESSAGE)
MSG.attach(p)


context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_SERVER,PORT,context=context) as server:
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, MSG['To'].split(","), MSG.as_string())