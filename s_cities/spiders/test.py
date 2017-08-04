# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Response, Request, FormRequest
from urllib import request


class TestSpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        yield FormRequest(
            'https://us.kompass.com/buy-company-list/filtervalues?CSRFToken=5edebdec-6b09-4303-b776-b154336e300c',
            method='POST',
            formdata={
                "filterCodeParam": "nomenclatureKompass", "freeCount": "true", "parentFieldParam": "01100"
            },
        )
    def parse(self, response):
        print(response.status)
        print(response.text)
        pass
