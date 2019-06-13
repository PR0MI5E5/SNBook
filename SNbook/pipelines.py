# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import logging
logger = logging.getLogger(__name__)

class SnbookPipeline(object):

    def open_spider(self, spider):
        client = MongoClient()
        self.collection = client["books"]["books"]

    def process_item(self, item, spider):
        if spider.name == "book":
            logger.warning("*"*100)
        print(item)
        logger.warning(item)
		self.collection.insert(dict(item))
        return item
	
	def close_spider(self,spider):
		self.client.close()
