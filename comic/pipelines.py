# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import json
from urllib.parse import to_bytes

import os
from scrapy import Request
import shutil

from scrapy.utils.project import get_project_settings

from .DB import Sqlite
from .items import CategoryItem, ComicItem, ChapterItem
from scrapy.pipelines.images import ImagesPipeline


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
        elif isinstance(item, ComicItem):
            Sqlite.insert_comic(item)
        elif isinstance(item, ChapterItem):
            Sqlite.insert_chapter(item)
        return item

headers = {
    'referer': "http://images.dmzj.com/",
    'user-agent': "Dalvik/2.1.0 (Linux; U; Android 8.0.0; MI 6 MIUI/8.10.25)",
    'connection': "Keep-Alive",
    'accept-encoding': "gzip",
    }


class MyImagePipeline(ImagesPipeline):
    img_store = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        if isinstance(item, CategoryItem):
            yield Request(item['category_cover'], headers=headers, meta={'path':'category'})
        elif isinstance(item, ComicItem):
            yield Request(item['cover'], headers=headers, meta={'path':'cover'})
        elif isinstance(item, ChapterItem):
            for url in item['page_urls']:
                yield Request(url, headers=headers, meta={'path':'comic/%s/%s' % (item['comic_id'], item['chapter_id'])})

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        item = request.meta
        new_path = item['path']
        # a = os.path.split(new_path)
        # if not os.path.exists(a[0]):
        #     os.makedirs(a[0])

        return '%s/%s' % (new_path, image_guid)

    def item_completed(self, results, item, info):
        paths = [x['path'] for ok, x in results if ok]
        if not paths:
            print("Item contains no images")
        else:
            if isinstance(item, ChapterItem):
                item['paths'] = json.dumps(paths)
                item['page_urls'] = json.dumps(item['page_urls'])
            else:
                item['cover_path'] = paths[0]
        return item


