import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import BookItem
from datetime import datetime
import re

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/']

    def parse(self, response:HtmlResponse):
        path = r"//div[@id='header-genres']//li[contains(@class,'b-header-md-shw-inline-block')]/following-sibling::li/a/@href | //div[@id='header-genres']//ul[@class='b-menu-second-container']/li[contains(@class,'b-menu-second-item')]/following-sibling::li[position()='2'][a]/a/@href"
        # path хранит ссылки на категории книг, которые в последсивии будем скрапить
        links_category_books = response.xpath(path).extract()
        for link in links_category_books:
           yield response.follow(link, callback=self.parse_books)

    def parse_books(self, response: HtmlResponse):
        next_page = response.xpath(r"//a[@class='pagination-next__text']/@href").extract_first()
        books_links = response.xpath(r"//div[@class='content-block-outer'][.//div[@class='desktop-subnavigagions-block only_desc']]//a[img]/@href").extract()

        for link in books_links:
            yield response.follow(link, callback=self.parse_block_books)
        yield response.follow(next_page, callback=self.parse_books)


    def convert_to_float(self,st):
        try:
            res = float(st)
        except ValueError:
            res = -1
        return res

    def parse_block_books(self, response:HtmlResponse):
        title_book = response.xpath(r'//div[@id="product-title"]/h1/text()').extract_first()
        title_book = re.findall(r':\s+(.+)', title_book)[0]
        authors_book = response.xpath(r'//div[@class="authors"][1]//a/text()').extract()
        rating_book = self.convert_to_float(response.xpath(r'//div[@id="rate"]/text()').extract_first())
        new_price = response.xpath(r'//span[@class="buying-pricenew-val-number"]/text()').extract_first()
        old_price = response.xpath(r'//span[@class="buying-priceold-val-number"]/text()').extract_first()
        current_price = response.xpath(r'//span[@class="buying-price-val-number"]/text()').extract_first()
        category = response.xpath(r'//div[@id="thermometer-books"]//a/span/text()').extract()
        if current_price:
            basic_price_book = self.convert_to_float(current_price)
            discounted_price_book = 0
        elif bool(new_price) and bool(old_price):
            basic_price_book = self.convert_to_float(old_price)
            discounted_price_book = self.convert_to_float(new_price)

        obj = {
            'discounted_price_book' : discounted_price_book,
            'basic_price_book' : basic_price_book,
            'authors_book' : authors_book,
            'title_book' : title_book,
            'link_book' : response.url,
            'rating_book': rating_book,
            'date_pars' : datetime.today(),
            'category' : category
        }

        yield BookItem(**obj)



















