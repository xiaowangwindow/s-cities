# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyHelloItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class RequestErrorItem(scrapy.Item):
    request_url = scrapy.Field()
    error_detail = scrapy.Field()


class CountryItem(scrapy.Item):
    continent_name = scrapy.Field()
    country_name = scrapy.Field()
    country_icon = scrapy.Field()
    country_description = scrapy.Field()
    country_url = scrapy.Field()

class CityItem(scrapy.Item):
    continent_name = scrapy.Field()
    country_name = scrapy.Field()
    province_name = scrapy.Field()
    city_name = scrapy.Field()
    city_native_name = scrapy.Field()
