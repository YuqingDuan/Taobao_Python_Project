# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

"""Add Storage Container Objects to items.py"""
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    # price = scrapy.Field()
    comment = scrapy.Field()
    now_price = scrapy.Field()
    address = scrapy.Field()
    sale_count = scrapy.Field()
    brand = scrapy.Field()
    produce = scrapy.Field()
    effect = scrapy.Field()
    pass


class TaobaoSpiderLoader(ItemLoader):
    default_item_class = TaobaoItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
