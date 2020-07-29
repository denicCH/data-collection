from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongo_base = client.instagramru
collection = mongo_base['instagram']


def pr_mongo(items):
    for key, item in items.items():
        print(key)
        for it in item:
            print(it)

query = {
    'subscriber': collection.find({'subscriber': {"$eq": 22212229670}}),  # //те кто подписаны на пользователя
    'subscriptions': collection.find({'subscriptions': {"$eq": 22212229670}})  # //те на кого подписан пользователь
}

pr_mongo(query)
