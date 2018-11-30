# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

""" Export data to JSON """
import json
import codecs
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi


class TaobaoPipeline(object):
    def __init__(self):
        self.file = codecs.open('taobao.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()


"""The database storage uses asynchronous operation in order to prevent the speed of inserting data 
from keeping up with the speed of crawling and parsing of web pages, resulting in blocking.
The Twisted framework is provided in Python to implement asynchronous operations.
The framework provides a connection pool through which data insertion into MySQL can be asynchronized."""


class TaobaoPipeline(object):
    # Linking database
    def __init__(self, ):
        dbparms = dict(host='127.0.0.1',
                       db='dangdang',
                       user='root',
                       passwd='Devilhunter9527',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor,
                       use_unicode=True,
                       )
        # Connection pool
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    # Using twisted to change insert operation in MySQL into asynchronous execution
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # Handling exceptions

    # Handling the exception of asynchronous insertion
    def handle_error(self, failure, item, spider):
        print(failure)

    # Perform specific insert operations
    def do_insert(self, cursor, item):
        # Import from item
        title = item['title'][0]
        link = item['link']
        # price = item['price'][0]
        comment = item['comment'][0]
        now_price = item['now_price']
        address = item['address']
        sale = item['sale_count']
        brand = item['brand'][0]
        produce = item['produce'][0]
        effect = item['effect'][0]

        print('title\t', title)
        print('link\t', link)
        # print('price\t', price)
        print('now_price\t', now_price)
        print('address\t', address)
        print('comment\t', comment)
        print('sale\t', sale)
        print('brand\t', brand)
        print('produce\t',  produce)
        print('effect\t', effect)

        try:
            sql = "insert into taob(title, link, comment, now_price, address, sale, brand, produce, effect) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (title, link, comment, now_price, address, sale, brand, produce, effect)
            cursor.execute(sql, values)
            print('Insert the data into database successfully!')
            print('------------------------------\n')
            return item

        except Exception as err:
            pass












