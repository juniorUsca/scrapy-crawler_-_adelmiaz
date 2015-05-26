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


class LarepublicaSpider(Spider):
    name = "larepublica"
    allowed_domains = ["larepublica.pe", "googleapis.com"]

    start = datetime.datetime.strptime("01-01-2013", "%d-%m-%Y")
    end = datetime.datetime.strptime("21-05-2015", "%d-%m-%Y")#18-05-2015
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    start_urls = []
    for date in reversed(date_generated):
        start_urls.append("http://www.larepublica.pe/marketing-y-publicidad/ultimas-noticias-"+date.strftime("%d-%m-%Y"))
        
    
    #start_urls = [
        #Gastronomia
        #"https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=es&prettyPrint=false&source=gcsc&gss=.pe&sig=cb6ef4de1f03dde8c26c6d526f8a1f35&cx=013803619059868835650:ri6kzichbws&q=gastronomia&googlehost=www.google.com&callback=google.search.Search.apiary1398&nocache=1430838648149"
        #Marketing
        #"http://www.larepublica.pe/marketing-y-publicidad/ultimas-noticias-27-04-2015",
        #"http://www.larepublica.pe/marketing-y-publicidad/ultimas-noticias-28-04-2015"
        #"http://www.larepublica.pe/marketing-y-publicidad"
    #]

    def parse(self, response):
        '''
        content = response.body_as_unicode()
        content = content[48:-2]
        jsonresponse = json.loads(content)
        news = jsonresponse["results"]
        items = []
        for new in news:
            item = New()
            item['tema'] = 'Gastronomia'
            item['titulo'] = new["title"]
            item['texto'] = new["content"]
            
            #item['fecha'] = new["title"]
            #item['name'] = site.xpath('a/text()').extract()
            #item['url'] = site.xpath('a/@href').extract()
            #item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)
        return items
        '''
        sel = Selector(response)
        sites = sel.xpath('//h2[@class="glr-list-item-title"]')
        for site in sites:
            item = Link()
            item['name'] = site.xpath('a/text()').extract()[0]
            item['url'] = site.xpath('a/@href').extract()[0]
            yield scrapy.Request(url=item['url'], callback=self.get_new)

    def parse_date(self, value):
        ### Formato LAREPUBLICA
        #Lunes, 27 de abril de 2015 | 8:09 am
        return datetime.datetime.strptime(value.encode('utf-8'),"%A, %d de %B de %Y | %I:%M %p").strftime("%d/%m/%Y")

    def get_new(self, response):
        sel = Selector(response)
        il = ItemLoader(item=New())
        il.add_value('tema', ['Marketing y Publicidad'])
        il.add_value('titulo', sel.xpath('//h1[@class="glr-post-title glr-mb-10"]/text()').extract())
        il.add_value('texto', sel.xpath('//div[@class="glr-post-entry"]').extract())
        il.add_value('fecha', sel.xpath('//span[@class="glr-left glr-post-date"]/text()').extract())
        il.add_value('keywords', sel.xpath('//div[@class="post-tags"]//a/text()').extract())
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

        '''
        item = New()
        item['tema'] = 'Marketing y Publicidad'
        item['titulo'] = self.parse_html(sel.xpath('//h1[@class="glr-post-title glr-mb-10"]/text()').extract()[0].strip())
        item['texto'] = self.parse_html(sel.xpath('//div[@class="glr-post-entry"]').extract()[0].strip())
        item['fecha'] = self.parse_date(sel.xpath('//span[@class="glr-left glr-post-date"]/text()').extract()[0].strip())
        '''
        #yield item
        '''res = []
        res.append({"tema" : item['tema'],"titulo" : item['titulo'] })
        with open('junior.json', 'w') as outfile:
                json.dump(res, outfile)
        yield item'''