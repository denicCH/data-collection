import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_parser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']


    def __init__(self, search, city):
        self.start_urls = [f'https://www.avito.ru/{city}?q={search}']
    def parse(self, response):
        ads_links = response.xpath("//h3/a[@class='snippet-link']")
        for link in ads_links:
           yield response.follow(link,callback=self.parse_ads)


    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(),response=response)
        loader.add_xpath('name',"//h1/span/text()")
        loader.add_xpath('photos',"//div[contains(@class,'gallery-img-wrapper')]/div/@data-url")
        loader.add_value('url', response.url)
        yield loader.load_item()




        # name = response.xpath("//h1/span/text()").extract_first()
        # photos = response.xpath("//div[contains(@class,'gallery-img-wrapper')]/div/@data-url").extract()
        # yield AvitoparserItem(name=name,photos=photos)
