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


class Peru21Spider(Spider):
    name = "peru21"
    allowed_domains = ["peru21.pe", "googleapis.com"]

    #start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    #end = datetime.datetime.strptime("12-05-2015", "%d-%m-%Y")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for cont in range(0,1350,15):#1300
        start_urls.append("http://peru21.buscamas.pe/marketing/?start="+str(cont))
    for cont in range(0,2450,15):#2400
        start_urls.append("http://peru21.buscamas.pe/publicidad/?start="+str(cont))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[contains(@class,"bloq_news")]')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('div/div/hgroup/h2/a/text()').extract()[0]
            item['url'] = site.xpath('div/div/hgroup/h2/a/@href').extract()[0]
            #item['url'] = "http://diariocorreo.pe/" + item['url']
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self, value):
        ### Formato PERU21
        #Sábado 25 de abril del 2015 | 12:40 
        return datetime.datetime.strptime(value.encode('utf-8'),"%A %d de %B del %Y | %H:%M ").strftime("%d/%m/%Y")
    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', sel.xpath('//h1[@itemprop="headline"]/a/text()').extract())
        il.add_value('texto', sel.xpath('//div[@itemprop="articleBody"]').extract())
        il.add_value('fecha', sel.xpath('//div[@itemprop="datePublished"]/text()').extract())
        il.add_value('keywords', sel.xpath('//div[contains(@class,"nota-tags")]//h3/a/text()').extract())
        item = il.load_item()

        if 'titulo' in item:
            pass
        else:
            iln = ItemLoader(item=New())
            iln.add_value('tema', ['Marketing y Publicidad'])
            iln.add_value('titulo', sel.xpath('//h1/text()').extract())
            iln.add_value('texto', sel.xpath('//div[@id="principal"]/div[@class="nota"]/div[3]').extract())
            iln.add_value('fecha', sel.xpath('//div[@class="fecha-nota"]/text()').extract())
            iln.add_value('keywords', sel.xpath('//div[contains(@class,"nota-tags")]//h3/a/text()').extract())
            item = iln.load_item()

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

