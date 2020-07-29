# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import re
import scrapy
from pymongo import MongoClient


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.instagramru
    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
    def __del__(self):
        self.client.close()


class LeroymerlinPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        img = item['photo']
        if img:
            try:
                yield scrapy.Request(img, meta=item)
            except Exception as e:
                print(e)


    def file_path(self, request, response=None, info=None):
        item = request.meta

        pattern = re.findall(r'/(\w+\.[a-z]{2,4})\?', request.url)
        pattern = pattern[0] if pattern else "None"
        full_name = " ".join(re.findall(r'(\w+)', item['full_name'] ))
        return f"{full_name}/{pattern}"
    def item_completed(self, results, item, info):
        if results:
            item['photo_local'] = results[0][1]['path'] if results[0] else "None"
        return item


class InstaparserPipeline(DataBasePipeline):
    def process_item(self, item, spider):
        item['_id'] = int(item['_id'])
        item['subscriber'] = list(map(int, item['subscriber']))
        item['subscriptions'] = list(map(int, item['subscriptions']))

        collection = self.mongo_base[spider.name]
        if collection.count_documents({'_id': item['_id']}) != 0:
            subscr = collection.find_one({'_id': item['_id']}, {'subscriber': 1, 'subscriptions': 1, "_id": 0})
            if subscr['subscriber'] != item['subscriber']:
                subscr['subscriber'] = list(set(subscr['subscriber']+item['subscriber']))
            if subscr['subscriptions'] != item['subscriptions']:
                subscr['subscriptions'] = list(set(subscr['subscriptions']+item['subscriptions']))
            collection.update_one({'_id': item['_id']}, {'$set': subscr})
        else:
            collection.insert_one(item)

        print(item)
        print(1)
        return item
