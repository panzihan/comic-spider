# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sqlite3

from .DB import Sqlite
from .items import CategoryItem


class ComicPipeline(object):



    # def __init__(self, sqlite_file, sqlite_table):
    #     self.sqlite_file = 'example.db'
    #     self.sqlite_table = 'comic'
    #
    # def from_crawler(cls, crawler):
    #

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            Sqlite.insert_category(item)
        else:
            Sqlite.insert_comic(item)
        return item


