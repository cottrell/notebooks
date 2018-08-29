#!/usr/bin/env python
import email
import getpass
import imaplib
import os
import sys
import argh

detach_dir = '.'


def get_attachments():
    user = input("Gmail username: ")
    pwd = getpass.getpass("Password: ")
    sender_email = input("Enter the sender's email (to filter by): ")

    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user, pwd)

    m.select("[Gmail]/All Mail")

    # If you get an error "command SEARCH illegal in state AUTH, only allowed in states SELECTED"
    # then it is likely that the mailbox you have tried to select doesn't exist.
    # If you were originally a Google Mail user (i.e. a user in the UK) then you should uncomment
    # the line below.

    # m.select("[Google Mail]/All Mail") # here you a can choose a mail box like INBOX instead

    # Alternatively you can search for emails in the inbox only
    # m.select("INBOX")

    # Use m.list() to get all the mailboxes

    resp, items = m.search(None, 'FROM', '"%s"' % sender_email)
    items = items[0].split()

    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)

        if mail.get_content_maintype() != 'multipart':
            continue

        subject = ""

        if mail["subject"] is not None:
            subject = mail["subject"]

        print(("[" + mail["From"] + "] :" + subject))

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            counter = 1

            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1

            att_path = os.path.join(detach_dir, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()


if __name__ == '__main__':
    argh.dispatch_command(get_attachments)
