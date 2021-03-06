#!/usr/bin/env python3

from sys import argv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib, ssl
from email import encoders
import configparser
import os
import re

# Generates a multipart MIME base class to be sent
def maildetach():
    #RECEIVER_EMAIL = config ['receiver']['receiver_email']
    Email_Regex = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    MSG = MIMEMultipart()
    MSG["Subject"] = input("Subject: ")
    mailpass= False
    while (not(mailpass)): 
        mailadss = input ("Enter a valid email address: ")
        mailarr = mailadss.split(", ")
        for mailad in mailarr:
            if (not Email_Regex.match(mailad)):
                mailpass= False
                print("For multiple addresses use 'example@mail.com, example2@mail.com'")
                break
            else:
                mailpass = True
    MSG["To"] = mailadss
    MESSAGE = MIMEText(input("Body: "))
    MSG.attach(MESSAGE)
    return MSG

# Read config
config = configparser.ConfigParser()
config.read("client.ini")
PORT = config ['server']['port']
SMTP_SERVER = config ['server']['smtp_server']
SENDER_EMAIL = config ['account']['mailaddr']
SENDER_PASS = config ['account']['password']


if(len(argv) < 2):
    MSG=maildetach()
else:
    # Process attachements passed by parameter
    MSG=maildetach()
    files = argv
    files.remove(files[0])
    for file in files:
        if(file):
            route = os.getcwd() + '/' + file
            attachment = open(route, "rb")
            # MIMEbase call to add Content-Type header
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" %file)
            MSG.attach(p)

# Connect to server using SMTP+SSL
context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_SERVER,PORT,context=context) as server:
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, MSG['To'].split(","), MSG.as_string())
