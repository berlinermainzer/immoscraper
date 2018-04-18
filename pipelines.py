# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import hashlib

class UrlDigesterPipeline(object):

    def process_item(self, item, spider):
        data = dict(item)
        digest = hashlib.md5(data['url'].encode("utf8")).hexdigest()
        data['url_hash'] = digest
        return data

class ImmoscraperJsonLinesPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

import pymongo

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self):
        self.mongo_uri = 'mongodb://localhost:27107/'
        self.mongo_db = 'immodb'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item        