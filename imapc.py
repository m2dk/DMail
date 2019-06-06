#!/usr/bin/env python3

from sys import argv, exit
from imapclient import IMAPClient

if(len(argv) < 4):
	print("Usage: ./imapc.py <IMAP server address> <email address> <password>")
	exit()

HOST = argv[1]
USERNAME = argv[2]
PASSWORD = argv[3]

with IMAPClient(HOST) as server:
    server.login(USERNAME, PASSWORD)
    server.select_folder('INBOX', readonly=True)
    server.idle()
    print("Connection is now IDLE, send email or quit with ^C")

    while(True):
        try:
            responses = server.idle_check(timeout=10) #10 segundos de espera
            print("Server sent:", responses if responses else "nothing")
            #TODO: get new messages when there's an IDLE timeout or new IDLE response.

            #messages = server.search('UNSEEN')
            #if(messages == None):
            #    print("No new mwssages")
            #for uid, message_data in server.fetch(messages, 'RFC822').items():
            #    email_message = email.message_from_bytes(message_data[b'RFC822'])
            #    print(uid, email_message)
        except KeyboardInterrupt:
            break

    server.idle_done()
