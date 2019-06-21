#!/usr/bin/env python3

from sys import exit
from imapclient import IMAPClient, SEEN
import email, configparser

config = configparser.ConfigParser()
config.read("client.ini")

HOST = config['server']['hostname']
USERNAME = config['account']['mailaddr']
PASSWORD = config['account']['password']
SET_READ = config['server']['setread'].lower()
TIMEOUT = float(config['server']['timeout'])

if(SET_READ == "false"):
    SET_READ = ""

with IMAPClient(HOST) as server:
    print("Establishing connection...")
    server.login(USERNAME, PASSWORD)
    # folder to watch: Inbox. Write access to mark as seen.
    server.select_folder('INBOX', readonly=False)
    print("Connection established.")
    while(True):
        try:
            server.idle()
            # blocking call to idle_check, times out at TIMEOUT seconds
            responses = server.idle_check(timeout=TIMEOUT)
            # exit IDLE mode to fetch mail headers
            server.idle_done()
            # searching only UNSEEN messages
            messages = server.search('UNSEEN')
            if(messages == None):
                print("No new messages.")
            else:
                print("Unseen mail:")
                # fetching message data from "messages" object
                for uid, message_data in server.fetch(messages, 'RFC822').items():
                    # transforming message data into email.message.Message object
                    email_message = email.message_from_bytes(message_data[b'RFC822'])
                    print("From:", email_message.get('From'), "Subject:", email_message.get('Subject'))
                # mark as unseen
                if not SET_READ:
                    server.remove_flags(messages, [SEEN])
        except KeyboardInterrupt:
            # logging out
            print("Closing connection...")
            server.logout()
            print("Connection closed.")
            exit()
