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


class CodigoSpider(Spider):
    name = "codigo"
    allowed_domains = ["www.codigo.pe", "googleapis.com"]

    #start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    #end = datetime.datetime.strptime("12-05-2015", "%d-%m-%Y")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for cont in range(0,100):#81
        start_urls.append("http://www.codigo.pe/marketing/page/"+str(cont))
    for cont in range(0,200):#141
        start_urls.append("http://www.codigo.pe/publicidad/page/"+str(cont))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//h4[contains(@class,"postimage-title")]')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('a/text()').extract()[0]
            item['url'] = site.xpath('a/@href').extract()[0]
            #item['url'] = "http://diariocorreo.pe/" + item['url']
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self, value):
        ### Formato CODIGO
        #23.08.2012
        return datetime.datetime.strptime(value.encode('utf-8'),"%d.%m.%Y").strftime("%d/%m/%Y")
    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', sel.xpath('//h1[@class="postTitle"]/text()').extract())
        il.add_value('texto', sel.xpath('//div[@class="post"]').extract())
        il.add_value('fecha', sel.xpath('//div[contains(@class,"post_fecha")]/text()').extract())
        il.add_value('keywords', sel.xpath('//p[contains(@class,"postMeta")]//a/text()').extract())
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

