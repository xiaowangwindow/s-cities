# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from twisted.python.failure import Failure
from typing import AnyStr

from s_cities.items import RequestErrorItem, CountryItem, CityItem
from s_cities.utils import parse_util


def generate_continent_url(continent: AnyStr) -> AnyStr:
    return 'https://www.citypopulation.de/{}.html'.format(continent)


class CitySpider(scrapy.Spider):
    name = "city"

    continent_list = [
        'Asia',
        # 'Africa', 'America', 'Europe', 'Oceania'
    ]

    def start_requests(self):
        for continent in self.continent_list:
            yield Request(
                generate_continent_url(continent),
                meta={'continent': continent},
                callback=self.parse_continent,
                errback=self.error_back,
            )

    def parse_continent(self, response: Response):
        soup = BeautifulSoup(response.text, 'lxml')
        for country_dict in parse_util.parse_continent(soup, response.url, response.meta['continent']):
            country_item = CountryItem(country_dict)
            yield country_item

            yield Request(
                country_item['country_url'],
                meta={
                    'continent': country_item['continent_name'],
                    'country': country_item['country_name']
                },
                callback=self.parse_country,
                errback=self.error_back,
            )

    def parse_country(self, response: Response):
        soup = BeautifulSoup(response.text, 'lxml')
        table_list = soup.find_all('table')
        if table_list and len(table_list) >= 2:
            # Case : https://www.citypopulation.de/Israel.html
            for city_dict in parse_util.parse_country_only_city(soup):
                city_item = CityItem(city_dict)
                city_item.setdefault('continent_name', response.meta.get('continent'))
                city_item.setdefault('country_name', response.meta.get('country'))
                city_item.setdefault('province_name', response.meta.get('province'))
                yield city_item
        elif table_list and len(table_list) == 1:
            # Case: https://www.citypopulation.de/php/armenia-admin.php
            for city_dict in parse_util.parse_country_contain_province(soup):
                city_item = CityItem(city_dict)
                city_item.setdefault('continent_name', response.meta.get('continent'))
                city_item.setdefault('country_name', response.meta.get('country'))
                city_item.setdefault('province_name', response.meta.get('province'))
                yield city_item
        else:
            country = soup.h1.string.lower()
            # Case: https://www.citypopulation.de/Bangladesh.html
            admin_url = soup.find('a', href=re.compile('php/\w+-admin.php$'))
            # Case: https://www.citypopulation.de/Russia.html
            state_a_list = soup.find_all('a', href=re.compile(r'php/{}-\w+-admin.php$'.format(country)))
            # Case: https://www.citypopulation.de/Croatia.html
            province_name_list = soup.find_all('a', href=re.compile(r'php/{}-\w+.php$'.format(country)))
            # Case: https://www.citypopulation.de/Uruguay.html
            cities_a = soup.find('a', href=re.compile(r'\w+-cities.html$', re.IGNORECASE))
            if admin_url:
                yield Request(
                    urljoin(response.url, admin_url['href']),
                    meta=response.meta,
                    callback=self.parse_country,
                    errback=self.error_back
                )
            elif state_a_list:
                for a in state_a_list:
                    yield Request(
                        urljoin(response.url, a['href']),
                        meta=response.meta,
                        callback=self.parse_country,
                        errback=self.error_back
                    )
            elif province_name_list:
                for a in province_name_list:
                    meta = response.meta
                    meta.update({'province': a.string})
                    yield Request(
                        urljoin(response.url, a['href']),
                        meta=meta,
                        callback=self.parse_country,
                        errback=self.error_back
                    )
            elif cities_a:
                yield Request(
                    urljoin(response.url, cities_a['href']),
                    meta=response.meta,
                    callback=self.parse_country,
                    errback=self.error_back
                )
            else:
                print(response.url)

    def error_back(self, failure: Failure):
        item = RequestErrorItem()
        item['request_url'] = failure.request.url
        item['error_detail'] = str(failure)
        yield item
