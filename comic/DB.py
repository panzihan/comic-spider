#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3

create_category_sql = '''
        CREATE TABLE IF NOT EXISTS "category" (
        "category_id" INTEGER PRIMARY KEY,
        "category_title" TEXT,
        "category_cover" TEXT,
        "cover_path" TEXT
    );
    '''

create_comic_sql = '''
  CREATE TABLE IF NOT EXISTS "comic" (
      "id" INTEGER PRIMARY KEY,
      "title" TEXT,
      "cover" TEXT,
      "cover_path" TEXT,
      "description" TEXT,
      "last_updatetime" INTEGER,
      "first_letter" TEXT,
      "authors" TEXT,
      "status" TEXT,
      "types" TEXT,
      "category_id" INTEGER REFERENCES category (category_id)
  )
  '''

create_chapter_sql = '''
    CREATE TABLE IF NOT EXISTS "chapter" (
        "comic_id" INTEGER,
        "chapter_id" INTEGER PRIMARY KEY,
        "title" TEXT,
        "chapter_title" TEXT,
        "chapter_order" INTEGER,
        "picnum" INTEGER,
        "page_urls" TEXT,
        "paths" TEXT,
        "updatetime" INTEGER
    )
'''

conn = sqlite3.connect('example.db')
cur = conn.cursor()
cur.execute(create_category_sql)
cur.execute(create_comic_sql)
cur.execute(create_chapter_sql)
# cur.execute('''
#     CREATE TABLE "status" (
#         "id" INTEGER PRIMARY KEY,
#         "name" TEXT
#     )
# ''')
# cur.execute('''
#     CREATE TABLE "author" (
#         "id" INTEGER PRIMARY KEY,
#         "name" TEXT
#     )
# ''')
# cur.execute('''
#     CREATE TABLE "type" (
#         "id" INTEGER PRIMARY KEY,
#         "name" TEXT
#     )
# ''')


class Sqlite(object):
    @classmethod
    def insert_comic(self, item):
        insert_sql = "Insert Or Replace into {0}({1}) values ({2})".format('comic',
                                                                           ', '.join(item.keys()),
                                                                           ', '.join(['?'] * len(item.keys())))
        cur.execute(insert_sql, list(item.values()))
        conn.commit()

    @classmethod
    def insert_category(self, item):
        insert_sql = " Insert Or Replace into {0}({1}) values ({2})".format('category',
                                                                            ', '.join(item.keys()),
                                                                            ', '.join(['?'] * len(item.keys())))
        cur.execute(insert_sql, list(item.values()))
        conn.commit()

    @classmethod
    def insert_chapter(self, item):
        insert_sql = " Insert Or Replace into {0}({1}) values ({2})".format('chapter',
                                                                            ', '.join(item.keys()),
                                                                            ', '.join(['?'] * len(item.keys())))
        cur.execute(insert_sql, list(item.values()))
        conn.commit()

    @classmethod
    def insert(self, name,  item):
        insert_sql = " Insert Or Replace into {0}({1}) values ({2})".format('chapter',
                                                                            ', '.join(item.keys()),
                                                                            ', '.join(['?'] * len(item.keys())))
        cur.execute(insert_sql, list(item.values()))
        conn.commit()

    @classmethod
    def query(self, comic_id):
        query_sql = 'select last_updatetime from comic where id = {0}'.format(comic_id)
        cursor = cur.execute(query_sql)
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return ''

    @classmethod
    def query_chapter(self, comic_id, chapter_id):
        query_sql = 'select updatetime from chapter where comic_id = {0} and chapter_id = {1}'.format(comic_id, chapter_id)
        cursor = cur.execute(query_sql)
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return ''
