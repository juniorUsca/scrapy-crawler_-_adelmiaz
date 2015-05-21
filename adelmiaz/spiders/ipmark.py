#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from scrapy.selector import Selector
import scrapy
import json
import re
from adelmiaz.items import New, Link
from scrapy.contrib.loader import ItemLoader
import datetime, locale
locale.setlocale(locale.LC_TIME, 'es_PE.utf8')


class IpmarkSpider(Spider):
    name = "ipmark"
    allowed_domains = ["ipmark.com", "googleapis.com"]

    #start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    #end = datetime.datetime.strptime("12-05-2015", "%d-%m-%Y")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for cont in range(1,470):#455
        start_urls.append("http://ipmark.com/page/"+str(cont)+"/?s=marketing")
    for cont in range(1,420):#415
        start_urls.append("http://ipmark.com/page/"+str(cont)+"/?s=publicidad")

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="posts"]')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('article/div/div/h1/a/text()').extract()[0]
            item['url'] = site.xpath('article/div/div/h1/a/@href').extract()[0]
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self, value):
        ### Formato IPMARK
        #19/05/2015 05:05
        value = value.strip()
        return datetime.datetime.strptime(value.encode('utf-8'),"%d/%m/%Y %H:%M").strftime("%d/%m/%Y")
    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', sel.xpath('//article[contains(@class,"post")]/header/h1/text()').extract())
        il.add_value('texto', [' '.join(sel.xpath('//div[@class="post-content"]/p').extract())] )
        il.add_value('fecha', sel.xpath('//div[contains(@class,"post-date")]/text()[3]').extract())
        il.add_value('keywords', sel.xpath('//div[contains(@class,"post-category")]/a/text()').extract())
        item = il.load_item()

        if 'titulo' in item:
            pass
        else:
            print item['titulo']
            print item['texto']

        if 'keywords' in item:
            pass
        else:
            item['keywords'] = ['Marketing y Publicidad']
        
        if 'fecha' in item:
            item['fecha'] = self.parse_date(item['fecha'])
        else:
            item['fecha'] = '10/05/2015'
        
        if 'titulo' in item:
            if 'texto' in item:
                yield item

