import scrapy


class BeyerSpider(scrapy.Spider):
    name = "beyer"
    start_urls = [
        'http://immobilien-bayer.de/01_efh-zfh-villen/',
    ]

    def parse(self, response):
        for offer in response.xpath("//div[@class='col-sm-6 col-md-4 immothumbs']"):
            print(offer)
            yield {
                'title': offer.xpath("h3/text()").extract_first().strip(),
                'url': offer.xpath('a/@href').extract_first()
            } 