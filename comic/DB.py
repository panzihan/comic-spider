#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3

create_category_sql = '''
        CREATE TABLE IF NOT EXISTS "category" (
        "category_id" INTEGER PRIMARY KEY,
        "category_title" TEXT,
        "category_cover" TEXT
    );
    '''

create_comic_sql = '''
  CREATE TABLE IF NOT EXISTS "comic" (
      "id" INTEGER PRIMARY KEY,
      "title" TEXT,
      "cover" TEXT,
      "description" TEXT,
      "last_updatetime" INTEGER,
      "first_letter" TEXT,
      "chapters" TEXT,
      "authors" TEXT,
      "types" TEXT,
      "category_id" INTEGER REFERENCES category (category_id)
  )
  '''

conn = sqlite3.connect('example.db')
cur = conn.cursor()
cur.execute(create_category_sql)
cur.execute(create_comic_sql)

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
    def query(self, comic_id):
        query_sql = 'select last_updatetime from comic where id = {0}'.format(comic_id)
        cursor = cur.execute(query_sql)
        data = cursor.fetchone()
        if data:
            return data[0]
        else:
            return ''