# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CategoryItem(scrapy.Item):
    category_id = scrapy.Field()
    category_title = scrapy.Field()
    category_cover = scrapy.Field()


class BaseComicItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    status = scrapy.Field()
    cover = scrapy.Field()
    types = scrapy.Field()
    last_updatetime = scrapy.Field()

class ComicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    category_id = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    description = scrapy.Field()
    last_updatetime = scrapy.Field()
    first_letter = scrapy.Field()
    chapters = scrapy.Field()
    authors = scrapy.Field()
    types = scrapy.Field()

