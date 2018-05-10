
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
        msg = text.render(data)

        logger.info(msg)

    def getData(self):

        data = [
            { "subject" : "ImmoScraper Report" },
            { "email_receivers" : ["xyz@gmail.com", "abc@gmail.com"] }
        ]

        for el in self.mongo_collection.find({'url_hash': 'ffd8505ea2340807fbb0e49ff1a5d23d'}):
            data.append({"entries" : el})

        return data

def main(argv):
    logger.info(argv)
        
    reporter = Reporter()

    elist = reporter.getData()

    for el in elist:
        pprint.pprint(el)
        #reporter.mailrender(el['data'], 'report')

    reporter.close()

if __name__ == "__main__":
    main(sys.argv)