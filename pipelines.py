# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import hashlib
from scrapy.exporters import JsonLinesItemExporter

class UrlDigesterPipeline(object):

    def process_item(self, item, spider):
        digest = hashlib.md5(item['url'].encode("utf8")).hexdigest()
        item['url_hash'] = digest
        return item

import datetime

class FirstSeenPipeline(object):

    def process_item(self, item, spider):
        item['first_seen'] = datetime.datetime.now()
        return item

class ImmoscraperJsonLinesPipeline(object):

    def open_spider(self, spider):
        file = open('items.jl', 'wb')
        self.jsonLineExporter = JsonLinesItemExporter(file) 

    def close_spider(self, spider):
        self.jsonLineExporter.finish_exporting()
        self.jsonLineExporter.file.close()

    def process_item(self, item, spider):
        self.jsonLineExporter.export_item(item)
        return item

import pymongo
import logging

class MongoPipeline(object):

    collection_name = 'items'

    def __init__(self):
        self.mongo_uri = 'mongodb://localhost'
        self.mongo_db = 'immodb'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[self.collection_name]
        logging.debug('Using db %s, %s', self.db, collection)
        
        cnt = collection.find({"url_hash": item['url_hash'] }).count()
        if cnt > 0:
            logging.debug('Skipping item %s, found it %i times', item['url_hash'], cnt)
        else:
            logging.debug('Inserting item %s', item['url_hash'])
            collection.insert_one(dict(item))
            
        return item        