# -*- coding: utf-8 -*-
import redis
import hashlib
import pymongo


class DuplicatesFilterPipeline(object):
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('REDIS_HOST'),
            port=crawler.settings.get('REDIS_PORT'),
            db=crawler.settings.get('REDIS_DB'),
            collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        self.pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True)
        self.conn = redis.Redis(connection_pool=self.pool)

    def process_item(self, item, spider):
        fingerprint = self.fingerprint(item)
        ret = self.conn.sadd(self.collection, fingerprint)
        if ret == 0:
            item['cjr_fingerprint'] = 'exist'  # 已存在
        return item

    def fingerprint(self, str):
        m1 = hashlib.md5()
        m1.update(str.encode("utf-8"))
        ret = m1.hexdigest()
        return ret


class MongoPipeline(object):
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MONGODB_HOST'),
            port=crawler.settings.get('MONGODB_PORT'),
            db=crawler.settings.get('MONGODB_DB'),
            collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.mydb = self.client[self.db]
        self.mycollection = self.mydb[self.collection]

    def process_item(self, item, spider):
        # if item.get('cjr_fingerprint') != 'exist':
        #     self.mycollection.insert(dict(item))
        self.mycollection.insert(dict(item))
        # self.mycollection.update_one(dict(item), {'$set': dict(item)}, upsert=True) #适用于数据量小的
        return item

    def close_spider(self, spider):
        self.client.close()
