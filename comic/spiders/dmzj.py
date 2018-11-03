# -*- coding: utf-8 -*-
import json
import logging

import scrapy

from ..DB import Sqlite
from ..items import CategoryItem, ComicItem, ChapterItem

# 所有分类列表
category_url = 'http://v3api.dmzj.com/0/category.json?channel=Android&version=2.7.009'
# 某一分类 漫画列表
comic_list_url = 'http://v3api.dmzj.com/classify/%s/1/%s.json?channel=Android&version=2.7.009'
# 某一漫画详情
comic_info_url = 'http://v3api.dmzj.com/comic/%s.json?channel=Android&version=2.7.009'
# 章节详情
chapter_url = 'http://v3api.dmzj.com/chapter/%s/%s.json?channel=Android&version=2.7.009'

class DmzjSpider(scrapy.Spider):
    name = 'dmzj'
    allowed_domains = ['v3api.dmzj.com']

    def start_requests(self):
        yield scrapy.Request(url=category_url, callback=self.get_category)
        # yield scrapy.Request(url='http://v3api.dmzj.com/chapter/9949/78012.json?channel=Android&version=2.7.009', callback=self.get_chapter)

    '''
    解析分类
    '''
    def get_category(self, response):
        for category in json.loads(response.text):
            tag = CategoryItem()
            tag['category_id'] = category['tag_id']
            tag['category_title'] = category['title']
            tag['category_cover'] = category['cover']
            yield tag
            url = comic_list_url % (tag['category_id'], 0)
            yield scrapy.Request(url=url, callback=self.get_comic, meta={'tag':tag})

    '''
    解析漫画列表
    '''
    def get_comic(self, response):
        tag = response.meta['tag']
        for comic in json.loads(response.text):
            url = comic_info_url % comic['id']
            time = Sqlite.query(comic_id=comic['id'])
            if time != comic['last_updatetime']:
                logging.debug('id %s name %s tag %s old %s  new %s 不一致 有更新' % (comic['id'] ,comic['title'] ,tag['category_title'] ,time, comic['last_updatetime']))
                yield scrapy.Request(url=url, callback=self.get_comic_info, meta={'tag':tag})
            else:
                logging.debug('last_updatetime %s 无更新' % comic['last_updatetime'])
            break

        # 下一页
        # next_page = int(str(response.url).split('/')[-1].split('.')[0])
        # url = comic_list_url % (tag['category_id'], next_page + 1)
        # yield scrapy.Request(url=url, callback=self.get_comic)

    '''解析详情'''
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
        item['authors'] = str(comic['authors'])
        item['types'] =  str(comic['types'])
        item['status'] =  str(comic['status'])
        item['category_id'] = tag['category_id']
        yield item
        for chapter in comic['chapters']:
            for data in chapter['data']:
                url = chapter_url % (item['id'], data['chapter_id'])
                yield scrapy.Request(url=url, callback=self.get_chapter, meta={'updatetime': data['updatetime'], 'title': chapter['title']})

    '''解析章节'''
    def get_chapter(self, response):
        title = response.meta['title']
        updatetime = response.meta['updatetime']
        chapter_json = json.loads(response.text)
        item = ChapterItem()
        item['comic_id'] = chapter_json['comic_id']
        item['chapter_id'] = chapter_json['chapter_id']
        item['title'] = title
        item['chapter_title'] = chapter_json['title']
        item['page_urls'] = chapter_json['page_url']
        item['picnum'] = chapter_json['picnum']
        item['chapter_order'] = chapter_json['chapter_order']
        item['updatetime'] = updatetime
        yield item