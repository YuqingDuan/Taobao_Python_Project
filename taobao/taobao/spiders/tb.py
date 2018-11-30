# -*- coding: utf-8 -*-

"""Crawler Programming tb.py"""
import scrapy
import re
from scrapy.http import Request
from taobao.items import TaobaoItem
import urllib.request
from scrapy_redis.spiders import RedisSpider


class TbSpider(RedisSpider):
    name = 'tb'
    # allowed_domains = ['taobao.com']
    # start_urls = ['http://taobao.com/']
    redis_key = 'Taobao:start_urls'

    def parse(self, response):
        key = input("Please input the keyword: \t")
        pages = input("Please input the pages: \t")
        print("\n")
        print("The keyword you input is: ", key)
        print("\n")

        for i in range(0, int(pages)):
            url = "https://s.taobao.com/search?q=" + str(key) + "&s=" + str(44 * i)
            yield Request(url=url, callback=self.page)
        pass

    # Searching page
    def page(self, response):
        body = response.body.decode('utf-8', 'ignore')

        pat_id = '"nid":"(.*?)"'  # matching id
        pat_now_price = '"view_price":"(.*?)"'  # matching now_price
        pat_address = '"item_loc":"(.*?)"'  # matching address
        pat_sale = '"view_sales":"(.*?)人付款"'  # matching sale

        all_id = re.compile(pat_id).findall(body)
        all_now_price = re.compile(pat_now_price).findall(body)
        all_address = re.compile(pat_address).findall(body)
        all_sale = re.compile(pat_sale).findall(body)

        for i in range(0, len(all_id)):
            this_id = all_id[i]
            now_price = all_now_price[i]
            address = all_address[i]
            sale_count = all_sale[i]
            url = "https://item.taobao.com/item.htm?id=" + str(this_id)
            yield Request(url=url,
                          callback=self.next,
                          meta={'now_price': now_price, 'address': address, 'sale_count': sale_count})
            pass
        pass

    # Detailed page
    def next(self, response):
        item = TaobaoItem()
        url = response.url

        # Because some of Taobao and Tianmao's information is loaded with Ajax in different ways, make a classification.
        if 'tmall' in url:  # Tianmao
            title = response.xpath("//html/head/title/text()").extract()  # title
            # price = response.xpath("//span[@class='tm-count']/text()").extract()
            # Here we get the original price of the commodity - but what we've been caught is the null value.
            # Xpath is validated in XPath finder.
            # I don't know why. Due to the subsequent impact on database writing, temporary deletion.
            # Following is the information acquisition in the product description information column,
            # retrieving text labels to obtain corresponding content:
            brand = response.xpath("//li[@id='J_attrBrandName']/text()").re('品牌:\xa0(.*?)$')  # brand
            produce = response.xpath("//li[contains(text(),'产地')]/text()").re('产地:\xa0(.*?)$')  # address
            effect = response.xpath("//li[contains(text(),'功效')]/text()").re('功效:\xa0(.*?)$')  # effect
            pat_id = 'id=(.*?)&'
            this_id = re.compile(pat_id).findall(url)[0]
            pass

        else:  # Taobao

            title = response.xpath("/html/head/title/text()").extract()  # title
            # price = response.xpath("//em[@class = 'tb-rmb-num']/text()").extract()
            # Here we get the original price of the commodity - but what we've been caught is the null value.
            # Xpath is validated in XPath finder.
            # I don't know why. Due to the subsequent impact on database writing, temporary deletion.
            # Following is the information acquisition in the product description information column,
            # retrieving text labels to obtain corresponding content:
            brand = response.xpath("//li[contains(text(),'品牌')]/text()").re('品牌:\xa0(.*?)$')  # brand
            produce = response.xpath("//li[contains(text(),'产地')]/text()").re('产地:\xa0(.*?)$')  # address
            effect = response.xpath("//li[contains(text(),'功效')]/text()").re('功效:\xa0(.*?)$')  # effect
            pat_id = 'id=(.*?)$'
            this_id = re.compile(pat_id).findall(url)[0]
            pass

        # Total number of comments
        comment_url = "https://rate.taobao.com/detailCount.do?callback=jsonp144&itemId=" + str(this_id)
        comment_data = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        each_comment = '"count":(.*?)}'
        comment = re.compile(each_comment).findall(comment_data)

        item['title'] = title
        item['link'] = url
        # item['price'] = price
        item['now_price'] = response.meta['now_price']
        item['comment'] = comment
        item['address'] = response.meta['address']
        item['sale_count'] = response.meta['sale_count']
        item['brand'] = brand
        item['produce'] = produce
        item['effect'] = effect

        yield item




















