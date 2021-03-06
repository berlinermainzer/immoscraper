import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from immoscraper.items import ImmoscraperItem

class BeyerSpider(scrapy.Spider):
    name = "BeyerSpider"
    start_urls = [
        'http://immobilien-bayer.de/01_efh-zfh-villen/',
    ]

    def parse(self, response):

        for offer in response.xpath("//div[@class='col-sm-6 col-md-4 immothumbs']"):
            #print(offer)
            l = ItemLoader(item=ImmoscraperItem(), response=response)
            #l.add_value('title', offer.xpath('h3/text()').extract_first().strip())
            l.add_value('url', offer.xpath('a/@href').extract_first())
            l.add_value('price', offer.xpath("div[1]/div[1]/div[2]/text()").extract_first().replace("€ ", "").replace(".", ""))
            l.add_value('house_type', offer.xpath("div[1]/div[2]/div[2]/text()").extract_first())
            l.add_value('size_house',  offer.xpath("div[1]/div[3]/div[2]/text()").extract_first().replace(" m²", ""))
            l.add_value('size_ground',  offer.xpath("div[1]/div[4]/div[2]/text()").extract_first().replace(" m²", ""))
            l.add_value('picture_url', offer.xpath('a/img/@src').extract_first())

            # follow link of url and get description
            desc_url = offer.xpath('a/@href').extract_first()
            request = scrapy.Request(desc_url, callback=self.parseDescription)
            request.meta['loader'] = l
            yield request
 

    def parseDescription(self, response):
        #print("################# getting desc")
        l = response.meta['loader']
        l.selector = Selector(response)
        
        desc = response.xpath('//*[@id="page"]/div[1]/div[4]/div[2]/p/text()').extract_first().strip()
        l.add_value('description', desc)

        title = response.xpath('//*[@id="page"]/div[1]/div[3]/div/h3/text()').extract_first().strip()
        l.add_value('title', title)
        
        return l.load_item()
        