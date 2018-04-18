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