#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Found at https://gist.github.com/jriguera/f3191528b7676bd60af5

# Python 3 and compatibility with Python 2
from __future__ import unicode_literals, print_function	

import os
import sys
import re
import logging
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotification(object):

    EMAIL_REGEX = re.compile('([\w\-\.\']+@(\w[\w\-]+\.)+[\w\-]+)')
    HTML_REGEX = re.compile('(^<!DOCTYPE html.*?>)')
    #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    #EMAIL_HOST = 'smtp.gmail.com'
    #EMAIL_USE_TLS = True
    #EMAIL_PORT=587
    
    def __init__(self, smtp, port, fromuser, fromemail, login=None, 
                 password=None, logger=None):
        self.logger = logger
        if not logger:
            logging.basicConfig()
            self.logger = logging.getLogger(__name__)
        self.smtp = smtp
        self.port = port
        self.mfrom = "%s <%s>" % (fromuser, fromemail)
        self.reply = fromemail
        self.smtplogin = login
        self.smtppass = password
       


    def _smtpconnect(self):
        try:
            self.logger.debug("Creating smtp")
            smtp = smtplib.SMTP(self.smtp, self.port)
            self.logger.debug("Connecting...")
            smtp.connect(self.smtp, self.port)
            self.logger.debug("TLSing...")
            smtp.starttls()
            #smtp.ehlo()
            #smtp.set_debuglevel(1)
        except Exception as e:
            self.logger.error("Cannot connect with '%s/%i': %s" % (self.smtp,self.port, e))
            raise
        if self.smtplogin:
            try:
                self.logger.debug("Login...")
                smtp.login(self.smtplogin, self.smtppass)
            except smtplib.SMTPException as e:
                self.logger.error("Cannot auth with '%s' on %s: %s" % (self.smtplogin, self.smtp, e))
                smtp.quit()
                raise
                
        return smtp

    def _smtpsend(self, smtp, recipient, subject, content):
        if self.HTML_REGEX.match(content) is None:
            self.logger.warn("Sending text mail to '%s'" % (recipient))
            msg = MIMEText(content)
        else:
            self.logger.warn("Sending html mail to '%s'" % (recipient))
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(content, 'html', 'utf-8'))
        msg['From'] = self.mfrom
        msg['To'] = recipient
        msg['Reply-to'] = self.reply
        msg['Subject'] = subject
        smtp.sendmail(self.mfrom, [recipient], msg.as_string())


    def send_email(self, recipient, subject, msg):
        smtp = self._smtpconnect()
        try:
            self._smtpsend(smtp, recipient, subject, msg)
        except smtplib.SMTPException as e:
            self.logger.error("Cannot send mail to '%s': %s" % (recipient, e))
            raise
        finally:
            smtp.quit()


    def send_bulk(self, msgs):
        self.logger.info('bulking')
        smtp = self._smtpconnect()
        processed = 0
        for (recipient, subject, msg) in msgs:
            try:
                self._smtpsend(smtp, recipient, subject, msg)
            except smtplib.SMTPException as e:
                self.logger.error("Cannot send mail to '%s': %s" % (recipient, e))
            else:
                processed += 1
        smtp.quit()
        self.logger.info('bulking done')

        return processed


  
import logging

logger = logging.getLogger('email_reporter')
logger.setLevel(logging.DEBUG)

def main(argv):
    #logger.warn(argv)

    fromemail = argv[1]
    login = fromemail
    password = argv[2]
    e = EmailNotification('mail.gmx.net', 587, 'Johannes Felten', fromemail, login, password, logger)
    
    e.send_email('johannesfelten@gmail.com', 'Hallo', 'Na, alles klar?')


if __name__ == "__main__":
    main(sys.argv)
