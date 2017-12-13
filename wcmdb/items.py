# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WcmdbItem(scrapy.Item):
    title = scrapy.Field()
    keywords = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    add_time = scrapy.Field()
    scrape_time = scrapy.Field()
    pass
