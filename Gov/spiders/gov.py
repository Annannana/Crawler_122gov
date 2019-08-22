# -*- coding: utf-8 -*-
import scrapy
import json
from Gov.items import GovItem

class GovSpider(scrapy.Spider):
    name = 'gov'

    def start_requests(self):
        with open('yanjie.txt', 'r') as file:
            for line in file.readlines():
                url = line.strip()
                yield scrapy.Request(url=url, callback=self.parse, meta={'link':url})

        # url = 'https://xuz.122.gov.cn/m/placesitectrl/loadBusincessList?page=1&size=119'
        # yield scrapy.Request(url=url, callback=self.parse,  meta={'link': url})

    def parse(self, response):
        link = response.meta.get('link')
        datas = json.loads(response.text)
        datas = datas.get('data')
        if datas:
            for data in datas.get('content'):
                item = GovItem()
                item["link"] = link
                item["officehour"] = data['gzsjfw']
                item["phone"] = [data['lxdh']]
                item["address"] = data['lxdz']
                item["city"] = data['fzjg']
                gps = data['gps']
                if gps:
                    gps = gps.split(',')
                    item["lng"] = gps[0]
                    item["lat"] = gps[1]
                item["name"] = data['wdmc']
                item["tag"] = data['ywfwms']
                yield item



