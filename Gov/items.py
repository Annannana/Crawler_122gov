# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GovItem(scrapy.Item):
    officehour = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    name = scrapy.Field()
    tag = scrapy.Field()
    link = scrapy.Field()
