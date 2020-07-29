# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    photo = scrapy.Field()
    subscriber = scrapy.Field()
    subscriptions = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    _id = scrapy.Field()
    photo_local = scrapy.Field()

