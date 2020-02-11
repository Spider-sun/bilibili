# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BilibiliPipeline(object):
    # def open_spider(self, spider):
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    db = client['bilibili']['tag_id']

    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        # 判断是否已经存在
        count = self.db.count_documents({'_id': item['_id']})
        # 若不存在
        if count == 0:
            self.db.insert_one(dict(item))
            print('插入数据：', item)
        return item