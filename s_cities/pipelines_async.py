
import pymongo
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem
from txmongo.connection import ConnectionPool
from twisted.internet import defer, reactor, ssl
from txmongo.filter import sort

from s_cities.items import CountryItem

class ScrapyCityPipeline(object):
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        return cls(crawler)

    def __init__(self, crawler: Crawler):
        self.crawler = crawler
        self.settings = crawler.settings

    @defer.inlineCallbacks
    def open_spider(self, spider):
        self.client = yield ConnectionPool(self.settings['MONGODB_URI'])
        self.db = self.client[self.settings['MONGODB_DB']]
        self.error_coll = self.db[self.settings['MONGODB_COLL_ERROR']]
        yield self.error_coll.create_index(sort([('request_url', 1)]))
        self.country_coll = self.db['country']
        o = sort([('continent_name',1), ('country_name', 1)])
        yield self.country_coll.create_index(o)


    @defer.inlineCallbacks
    def close_spider(self, spider):
        yield self.client.disconnect()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        if isinstance(item, CountryItem):
            yield self.country_coll.insert_one(dict(item))
        return item

if __name__ == '__main__':
    pass