# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.vacansy123


    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)



        # salary = item['salary']
        # item['salary_min'],item['salary_max'],item['currency'] = self.process_salary(salary)
        # del item['salary']


        return item

    def __del__(self):
        self.client.close()


    # def process_salary(self, salary):
    #     pass