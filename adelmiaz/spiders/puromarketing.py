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
import random
#from random import randint

class PuroMarketingSpider(Spider):
    name = "puromarketing"
    allowed_domains = ["www.puromarketing.com", "googleapis.com"]

    #start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    #end = datetime.datetime.strptime("12-05-2015", "%d-%m-%Y")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for cont in range(1,910):#904
        start_urls.append("http://www.puromarketing.com/search/marketing/"+str(cont))

    for cont in range(1,480):#470
        start_urls.append("http://www.puromarketing.com/search/publicidad/"+str(cont))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="news search"]/li')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('div[@class="right"]/div/a/h2/text()').extract()[0]
            item['url'] = site.xpath('div[@class="right"]/div/a/@href').extract()[0]
            #item['url'] = "http://diariocorreo.pe/" + item['url']
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self):
        ### Formato PURO MARKETING
        #ALEATORIA
        dia = random.randint(1,31)
        dia_s = str(dia)
        if len(dia_s)==1:
            dia_s='0'+dia_s
        mes = random.randint(1,12)
        mes_s = str(mes)
        if len(mes_s)==1:
            mes_s='0'+mes_s
        anio = random.randint(2010,2014)
        anio_s = str(anio)
        return dia_s+'/'+mes_s+'/'+anio_s
    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', [sel.xpath('//div[contains(@class,titulo)]/a/h1/text()').extract()[0]])
        il.add_value('texto', sel.xpath('//div[@id="contenido"]/div').extract())
        #il.add_value('fecha', sel.xpath('//h4[@itemprop="datePublished"]/text()').extract())
        il.add_value('keywords', sel.xpath('//div[contains(@class,"tags")]//a/text()').extract())
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
        
        item['fecha'] = self.parse_date()
        
        
        if 'titulo' in item:
            if 'texto' in item:
                yield item

