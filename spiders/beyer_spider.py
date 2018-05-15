import scrapy
from scrapy.loader import ItemLoader
from immoscraper.items import ImmoscraperItem

class BeyerSpider(scrapy.Spider):
    name = "beyer"
    start_urls = [
        'http://immobilien-bayer.de/01_efh-zfh-villen/',
    ]

    def parse(self, response):
    
        for offer in response.xpath("//div[@class='col-sm-6 col-md-4 immothumbs']"):
            #print(offer)
            l = ItemLoader(item=ImmoscraperItem(), response=response)
            l.add_value('title', offer.xpath('h3/text()').extract_first().strip())
            l.add_value('url', offer.xpath('a/@href').extract_first())
            l.add_value('price', offer.xpath("div[1]/div[1]/div[2]/text()").extract_first().replace("€ ", "").replace(".", ""))
            l.add_value('house_type', offer.xpath("div[1]/div[2]/div[2]/text()").extract_first())
            l.add_value('size_house',  offer.xpath("div[1]/div[3]/div[2]/text()").extract_first().replace(" m²", ""))
            l.add_value('size_ground',  offer.xpath("div[1]/div[4]/div[2]/text()").extract_first().replace(" m²", ""))
            l.add_value('picture_url', offer.xpath('a/img/@src').extract_first())
            # TODO: follow link of url and get description 
            l.add_value('description', 'n/a')
            yield l.load_item()
        