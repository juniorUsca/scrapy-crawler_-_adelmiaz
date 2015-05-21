#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

class AdelmiazItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Link(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

class New(scrapy.Item):
    tema = scrapy.Field(
        output_processor=Join(),
    )
    titulo = scrapy.Field(
    	input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    texto = scrapy.Field(
    	input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    fecha = scrapy.Field(
        #input_processor=MapCompose(parse_date),
        output_processor=Join(),
    )
    keywords = scrapy.Field()