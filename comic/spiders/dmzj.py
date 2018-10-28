# -*- coding: utf-8 -*-
import json
import logging

import scrapy

from ..DB import Sqlite
from ..items import CategoryItem, ComicItem


class DmzjSpider(scrapy.Spider):
    name = 'dmzj'
    allowed_domains = ['v3api.dmzj.com']

    def start_requests(self):
        url = 'http://v3api.dmzj.com/0/category.json'
        yield scrapy.Request(url=url, callback=self.get_category)

    '''
    获取分类
    '''
    def get_category(self, response):
        for category in json.loads(response.text):
            tag = CategoryItem()
            tag['category_id'] = category['tag_id']
            tag['category_title'] = category['title']
            tag['category_cover'] = category['cover']
            yield tag
            url = 'http://v3api.dmzj.com/classify/%s/1/0.json' % tag['category_id']
            yield scrapy.Request(url=url, callback=self.get_comic, meta={'tag':tag})
            # break

    '''
    获取漫画列表
    '''
    def get_comic(self, response):
        tag = response.meta['tag']
        for comic in json.loads(response.text):
            url = 'http://v3api.dmzj.com/comic/%s.json' % comic['id']
            time = Sqlite.query(comic_id=comic['id'])
            if time != comic['last_updatetime']:
                logging.debug('old %s  new %s 不一致 有更新' % (time, comic['last_updatetime']))
                yield scrapy.Request(url=url, callback=self.get_comic_info, meta={'tag':tag})
            else:
                logging.debug('last_updatetime %s 无更新' % comic['last_updatetime'])
            # break

        # 下一页
        next_page = int(str(response.url).split('/')[-1].split('.')[0])
        url = 'http://v3api.dmzj.com/classify/%s/0/%s.json' % (tag['category_id'], next_page + 1)
        # yield scrapy.Request(url=url, callback=self.get_comic)

    '''详情'''
    def get_comic_info(self, response):
        tag = response.meta['tag']
        comic = json.loads(response.text)
        item = ComicItem()
        item['id'] = int(comic['id'])
        item['title'] = comic['title']
        item['cover'] = comic['cover']
        item['description'] = comic['description']
        item['last_updatetime'] = comic['last_updatetime']
        item['first_letter'] = comic['first_letter']
        item['chapters'] = str(comic['chapters'])
        item['authors'] = str(comic['authors'])
        item['types'] = str(comic['types'])
        item['category_id'] = tag['category_id']
        return item