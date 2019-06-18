from sys import exit
from imapclient import IMAPClient, SEEN
import smtplib , ssl
import email, configparser

config = configparser.ConfigParser()
config.read("client.ini")

PORT = config ['server']['port']
SMTP_SERVER = config ['server']['smtp_server']
RECEIVER_EMAIL = config ['receiver']['receiver_email']
SENDER_EMAIL = config ['account']['mailaddr']
SENDER_PASS = config ['account']['password']

MESSAGE = config ['receiver']['message']

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_SERVER,PORT,context=context) as server:
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE)