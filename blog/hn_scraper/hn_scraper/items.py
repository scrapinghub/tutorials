# -*- coding: utf-8 -*-
import scrapy


class HnArticleItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
