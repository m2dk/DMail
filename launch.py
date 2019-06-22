#!/usr/bin/env python3

import os
import sys
import signal

print("DMail - Direct Mail suite")
print("Make sure you configured your client first!")
while(True):
    pid = -1
    try:
        # Menu print
        print("1. I want to monitor my INBOX folder")
        print("2. I want to send mail")
        print("Press 'q' to quit")
        command = input(">> ")
        # For every command we do a fork-exec-wait to come back to the parent process
        # sys.executable is just the python interpreter that is currently being used
        if(command == '1'):
            pid = os.fork()
            if(pid):
                os.waitpid(pid, 0)
            else:
                os.execv(sys.executable, [sys.executable] + ["imap.py"])

        elif(command == '2'):
            args = input("Do you want to send attachments? If so, write the filenames here (else, just press\
 enter): ")
            args = args.strip()
            pid = os.fork()
            if(pid):
                os.waitpid(pid, 0)
            else:
                os.execv(sys.executable, [sys.executable] + ["smtp.py"] + args.split(' '))

        elif(command == 'q'):
            sys.exit()
        else:
            print("Command not recognized, try again!")

    # Handles ^C to kill child without killing the parent process.
    except KeyboardInterrupt:
        if not (pid == -1 or pid == 0):
            os.kill(pid, signal.SIGHUP)
        else:
            print('')
            pass
