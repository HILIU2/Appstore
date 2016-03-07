# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppstoresplashItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title = scrapy.Field()
	thumbnail_url = scrapy.Field()
	url = scrapy.Field()
	appid = scrapy.Field()
	intro = scrapy.Field()
	recommended = scrapy.Field()
	pass
