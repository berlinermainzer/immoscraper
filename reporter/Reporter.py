
from jinja2 import Environment, FileSystemLoader
import os
import sys
import logging

logging.basicConfig()
logger = logging.getLogger('Reporter')
logger.setLevel(10)

class Reporter(object):
    
    def __init__(self, templatedir='templates'):

        if os.path.isdir(templatedir):
            self.templatedir = templatedir
        else:
            self.templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), templatedir)
        self.env = Environment(loader=FileSystemLoader(self.templatedir))


    def _mailrender(self, data, template):
        template = template + ".tmpl"
        logger.info("Rendering template '%s'" % (template))
        text = self.env.get_template(template)
        msg = text.render(data)

        logger.info(msg)



def main(argv):
    logger.info(argv)
    
    elist = [{
        "email": "xyz@gmail.com",
        "subject": "ImmoScraper Report",
        "data" : { 
            "dear": "Johannes",
            "msg": "Hola mundo"
        }
    },
        {
        "email": "abc@gmail.com",
        "subject": "ImmoScraper Report",
        "data" : { 
            "dear": "Kerstin",
            "msg": "Na, du Süße?"
        }
    }]

    reporter = Reporter()

    for el in elist:
        reporter._mailrender(el['data'], 'report')

if __name__ == "__main__":
    main(sys.argv)