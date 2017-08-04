# -*- coding: utf-8 -*-

import pymongo
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem

from sm_save_html_source.items import SM_SaveHTMLSourceItem


class SM_SaveHTMLSourcePipeline(object):
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        return cls(crawler)

    def __init__(self, crawler: Crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.settings['MONGODB_URI'])
        self.db = self.client[self.settings['MONGODB_DB']]
        self.coll = self.db[self.settings['MONGODB_COLL_RAW']]
        self.coll.create_index('request_url')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, SM_SaveHTMLSourceItem):
            self.coll.update_one(
                {'request_url': item['request_url']},
                {'$set': dict(item)},
                upsert=True
            )
            raise DropItem
        else:
            return item


if __name__ == '__main__':
    pass
