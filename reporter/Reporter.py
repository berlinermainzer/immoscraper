#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import os
import sys
import logging
import pymongo
import pprint
from EmailNotification import EmailNotification
import datetime

logging.basicConfig()
logger = logging.getLogger('Reporter')
logger.setLevel(logging.INFO)

class Reporter(object):
    

    def __init__(self, templatedir='templates', mongo_uri='mongodb://localhost', mongo_db = 'immodb', mongo_collection_name = 'items'):
        if os.path.isdir(templatedir):
            self.templatedir = templatedir
        else:
            self.templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), templatedir)
        self.env = Environment(loader=FileSystemLoader(self.templatedir))

        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[mongo_db]
        self.mongo_collection = self.mongo_db[mongo_collection_name]

    def close(self):
        self.mongo_client.close()

    def mailrender(self, data, template):
        template = template + ".tmpl"
        logger.info("Rendering template '%s'" % (template))
        text = self.env.get_template(template)

        msg = text.render(data=data)
        return msg


    def getData(self):

        entries = []
        #testing only 2 entries-- for el in self.mongo_collection.find({'url_hash' : { '$in' : ['c8a3d1d28fc3e53cc28bbc6852bf2ae4', 'a180fc4903e1e197ce17dedc2b3b2edd']}}):
        for el in self.mongo_collection.find({'has_been_reported' : True}): # Pull only new entries from the db
            entries.append(el)
            el['has_been_reported'] = False
            self.mongo_collection.save(el)

        logger.info('Found %d new entries.', len(entries))
		
        data = {
            'now' : datetime.datetime.utcnow,
            'subject' : 'ImmoScraper Report',
            'email_receivers' : [
                { 'name' : 'Johannes', 'email' : 'johannesfelten@gmail.com'}
            ],
            'entries' : entries
        }
		
        return data

def main(argv):

    fromemail = argv[1]
    login = fromemail
    password = argv[2]
    emailNotifyer = EmailNotification('mail.gmx.net', 587, 'Johannes Felten', fromemail, login, password, logger)
    
    reporter = Reporter()
    data = reporter.getData()

    email_receivers = data.pop('email_receivers')
    for receiver in email_receivers:
        logger.debug('---- Receiver: ' + receiver['name'])

        # Add receiver name to template data
        render_data = data
        render_data['name'] = receiver['name']

        # Render message
        msg = reporter.mailrender(render_data, 'report')
        logger.debug(msg)

        emailNotifyer.send_email(receiver['email'], 'ImmoScraper Report', msg)

    reporter.close()



if __name__ == "__main__":
    main(sys.argv)