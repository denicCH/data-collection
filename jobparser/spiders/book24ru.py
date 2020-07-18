import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import BookItem
from datetime import datetime
import re

class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/']

    def parse(self, response:HtmlResponse):
        path = r'//ul[@class="menu-catalog-new-d__list _parent"]/li/preceding-sibling::li[8]/a/@href'
        # path хранит ссылки на категории книг, которые в последсивии будем скрапить
        links_category_books = response.xpath(path).extract()
        for link in links_category_books:
            yield response.follow(link, callback=self.parse_books)

    def parse_books(self, response: HtmlResponse):
        next_page = response.xpath(r'//a[@class="catalog-pagination__item _text js-pagination-catalog-item"][last()]/@href').extract_first()
        books_links = response.xpath(r'//a[@class="book__image-link js-item-element ddl_product_link"]/@href').extract()

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

        title_book = response.xpath(r'//h1[@class="item-detail__title"]/text()').extract_first()
        authors_book = response.xpath(r'//div[@class="item-tab__chars-item"][1]/span[@class="item-tab__chars-value"][a]/a/text() | //div[@class="item-tab__chars-item"][1]/span[@class="item-tab__chars-value"][not(a)]/text()').extract_first()
        authors_book = authors_book.split(", ")
        rating_book = response.xpath(r'//span[@class="rating__rate-value"]/text()').extract_first()
        rating_book = self.convert_to_float(rating_book.replace(",",".")) if rating_book else None
        new_price = response.xpath(r'//div[@class="item-actions__prices"]/div[@class="item-actions__price"]/b/text()').extract_first()
        old_price = response.xpath(r'//span[@class="buying-priceold-val-number"]/text()').extract_first()
        current_price = response.xpath(r'//div[@class="item-actions__prices"]/div[@class="item-actions__price-old"]/text()').extract_first()
        category = response.xpath(r'//div[@class="breadcrumbs__list"]/div[a]/following-sibling::div[a][1]/a/text()').extract()
        basic_price_book = 0
        discounted_price_book = 0

        if bool(new_price) and bool(old_price):
            basic_price_book = self.convert_to_float(old_price)
            discounted_price_book = self.convert_to_float(new_price)
        elif bool(new_price):
            basic_price_book = self.convert_to_float(new_price)

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























