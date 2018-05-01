# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class ImmoscraperItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    url_hash = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    house_type = scrapy.Field(output_processor=TakeFirst())
    size_house = scrapy.Field(output_processor=TakeFirst())
    size_ground = scrapy.Field(output_processor=TakeFirst())
    picture_url = scrapy.Field(output_processor=TakeFirst())
    reported = scrapy.Field(output_processor=TakeFirst())
    first_seen = scrapy.Field(output_processor=TakeFirst())
    has_been_reported = scrapy.Field(output_processor=TakeFirst())

 