# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    else:
        return value

def transformation_to_float(value):
    q = value[0]
    if not(type(q) == type("value")):
        for key in q.keys():
            try:
                q[key] = float(q[key])
            except ValueError:
                pass
    else:
            try:
                q = float(q)
            except ValueError:
                pass
    return q


class leroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:

    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(output_processor=transformation_to_float)
    characteristics = scrapy.Field(output_processor=transformation_to_float)
    url = scrapy.Field(output_processor=TakeFirst())
    date_pars = scrapy.Field(output_processor=TakeFirst())

