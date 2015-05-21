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


class DiarioCorreoSpider(Spider):
    name = "diariocorreo"
    allowed_domains = ["diariocorreo.pe", "googleapis.com"]

    #start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    #end = datetime.datetime.strptime("12-05-2015", "%d-%m-%Y")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for cont in range(1,61):#51
        start_urls.append("http://www.diariocorreo.pe/buscar/?q=marketing&page="+str(cont))
    for cont in range(1,150):#130
        start_urls.append("http://www.diariocorreo.pe/buscar/?q=publicidad&page="+str(cont))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//article[@class="search-news"]')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('a/h2[@itemprop="headline"]/text()').extract()[0]
            item['url'] = site.xpath('a/@href').extract()[0]
            item['url'] = "http://www.diariocorreo.pe/" + item['url']
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self, value):
        ### Formato DIARIOCORREO
        #11 de Febrero del 2015 - 17:26 | Berlín
        value = value.split('|')[0]
        print value
        return datetime.datetime.strptime(value.encode('utf-8'),"%d de %B del %Y - %H:%M ").strftime("%d/%m/%Y")

    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', sel.xpath('//h1[@itemprop="headline"]/text()').extract())
        il.add_value('texto', sel.xpath('//div[@class="description-news"]').extract())
        il.add_value('fecha', sel.xpath('//span[@class="date-city"]/text()').extract())
        il.add_value('keywords', sel.xpath('//ul[@id="tags"]//a/text()').extract())
        item = il.load_item()
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
