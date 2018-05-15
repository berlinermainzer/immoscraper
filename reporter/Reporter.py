
from jinja2 import Environment, FileSystemLoader
import os
import sys
import logging
import pymongo
import pprint


logging.basicConfig()
logger = logging.getLogger('Reporter')
logger.setLevel(10)

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
        for el in self.mongo_collection.find({'url_hash' : { '$in' : ['dfb8cf90b7a48f51dd4ce179b57f4ee6', '80fcd534eb9b341a09b7f85f22c3a3e7']}}):
            entries.append(el)

        data = {
            'subject' : 'ImmoScraper Report',
            'email_receivers' : [
                { 'name' : 'Johannes', 'email' : 'xyz@gmail.com'},
                { 'name' : 'Kerstin', 'email' : 'abc@gmail.com'}
            ],
            'entries' : entries
        }

        return data

def main(argv):
    logger.info(argv)
        
    reporter = Reporter()

    data = reporter.getData()

    email_receivers = data.pop('email_receivers')
    for receiver in email_receivers:
        logger.info('---- Receiver: ' + receiver['name'])

        # Add receiver name to template data
        render_data = data
        render_data['name'] = receiver['name']

        # Render message
        msg = reporter.mailrender(render_data, 'report')
        
        logger.info(msg)

    reporter.close()

if __name__ == "__main__":
    main(sys.argv)