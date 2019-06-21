# DMail
Direct Mail - suite of email related utilities for a Data Comms course. It
includes:

* imap.py ~ IMAP client, watches over the INBOX folder using IMAP IDLE.

* smtp.py ~ SMTP cliet, sends mail with attachments

## Dependencies
imapclient 2.1.0-py3

## Usage
* imap.py: set up all the relevant fields in `client.ini`, and then run 
`./imap.py` in your terminal. It should monitor your INBOX folder and notify
if there are unseen messages in it.

* smtp.py: set up all the relevant fields in `client.ini`, and then run
`./smtp.py` in your terminal. Optionally, you can send attachments by passing
filenames as parameters. It will ask for subject, destination address and
body of the mail.
