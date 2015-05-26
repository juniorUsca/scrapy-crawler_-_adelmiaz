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


class ElComercioSpider(Spider):
    name = "elcomercio"
    allowed_domains = ["elcomercio.pe", "googleapis.com"]

    #start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    #end = datetime.datetime.strptime("12-05-2015", "%d-%m-%Y")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for cont in range(0,650,15):#600
        start_urls.append("http://elcomercio.pe/buscar/marketing/?start="+str(cont))
    for cont in range(0,1450,15):#1400
        start_urls.append("http://elcomercio.pe/buscar/publicidad/?start="+str(cont))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="bloq_news"]')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('div/div/hgroup/h2/a/text()').extract()[0]
            item['url'] = site.xpath('div/div/hgroup/h2/a/@href').extract()[0]
            #item['url'] = "http://diariocorreo.pe/" + item['url']
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self, value):
        ### Formato ELCOMERCIO
        #2013-01-10
        return datetime.datetime.strptime(value.encode('utf-8'),"%Y-%m-%d").strftime("%d/%m/%Y")

    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', sel.xpath('//h1[@itemprop="headline"]/text()').extract())
        il.add_value('texto', sel.xpath('//div[@itemprop="articleBody"]').extract())
        il.add_value('fecha', sel.xpath('//meta[@itemprop="datePublished"]/@content').extract())
        il.add_value('keywords', sel.xpath('//div[@class="nota-tags"]//h2/a/text()').extract())
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