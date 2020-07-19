import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_parser.items import leroymerlinparserItem
from scrapy.loader import ItemLoader
from datetime import datetime
class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?sortby=8&page=1&tab=products&q={search}']

    def parse(self, response):
        ads_links = response.xpath('//a[@class="link-wrapper"]')
        button_link = response.xpath('//a[@rel="next"]/@href')[0]

        for link in ads_links:
           yield response.follow(link,callback=self.parse_ads)
        print(1)
        yield response.follow(button_link, callback=self.parse)

    def parse_ads(self, response:HtmlResponse):

        ch = response.xpath('//section[@id="nav-characteristics"]//div[@class="def-list__group"]')
        characteristics = {item.xpath('normalize-space(.//dt/text())').extract_first():item.xpath('normalize-space(.//dd/text())').extract_first() for item in ch}


        loader = ItemLoader(item=leroymerlinparserItem(), response=response)

        loader.add_xpath('name','//h1[@slot="title"]/text()')
        loader.add_xpath('photos','//picture[@slot="pictures"]/img/@src')
        loader.add_xpath('price','//meta[@itemprop="price"]/@content')
        loader.add_value('url', response.url)
        loader.add_value('characteristics', characteristics)
        loader.add_value('date_pars', datetime.today())

        yield loader.load_item()

