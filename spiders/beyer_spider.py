import scrapy


class BeyerSpider(scrapy.Spider):
    name = "beyer"
    start_urls = [
        'http://immobilien-bayer.de/01_efh-zfh-villen/',
    ]

    def parse(self, response):
        for offer in response.xpath("//div[@class='col-sm-6 col-md-4 immothumbs']"):
            #print(offer)
            yield {
                'title': offer.xpath('h3/text()').extract_first().strip(),
                'url': offer.xpath('a/@href').extract_first(),
                'price': offer.xpath("div[1]/div[1]/div[2]/text()").extract_first().replace("€ ", "").replace(".", ""),
                'type': offer.xpath("div[1]/div[2]/div[2]/text()").extract_first(),
                'size_house':  offer.xpath("div[1]/div[3]/div[2]/text()").extract_first().replace(" m²", ""),
                'size_ground':  offer.xpath("div[1]/div[4]/div[2]/text()").extract_first().replace(" m²", ""),
                'picture_url': offer.xpath('a/img/@src').extract_first(),
            } 
