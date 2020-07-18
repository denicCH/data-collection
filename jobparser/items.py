import scrapy

class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    text_vac = scrapy.Field()
    link_vac = scrapy.Field()
    date_pars = scrapy.Field()
    company = scrapy.Field()
    name_vac = scrapy.Field()

class BookItem(scrapy.Item):
    _id = scrapy.Field()
    discounted_price_book = scrapy.Field()
    basic_price_book = scrapy.Field()
    title_book = scrapy.Field()
    link_book = scrapy.Field()
    rating_book = scrapy.Field()
    date_pars = scrapy.Field()
    authors_book = scrapy.Field()
    category = scrapy.Field()

