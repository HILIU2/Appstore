import scrapy
import re
from scrapy.selector import Selector
from appstoresplash.items import AppstoresplashItem
from scrapy.spiders import Spider

class HWSpider(scrapy.Spider):
	name = "huawei_splash"
	allowed_domains = ["huawei.com"]

	start_urls = [
		"http://appstore.huawei.com/more/all"
	]

	def parse(self, response):
		page = Selector(response)

		hrefs = page.xpath('.//h4[@class="title"]/a/@href')

		for href in hrefs:
			url = href.extract()
			yield scrapy.Request(url, self.parse_item, meta = { 
				'splash':{
					'endpoint': 'render.html',
					'args': {'wait': 5.5}
				}
			})

	def parse_item(self, response):
		page = Selector(response)
		item = AppstoresplashItem()

		appinfo = page.xpath('//ul[@class="app-info-ul nofloat"]')

		item['title'] = appinfo.xpath('.//li/p/span[@class="title"]/text()').extract_first().encode('utf-8')
		item['url'] = response.url
		item['thumbnail_url'] = appinfo.xpath('.//li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first()
		item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
		item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8')

		divs = page.xpath('//div[@class="open-info"]')
		recomm = ""
		for div in divs:
			url = div.xpath('./p[@class="name"]/a/@href').extract_first()
			recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
			name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
			recomm += "{0}:{1},".format(recommended_appid, name)

		item['recommended'] = recomm

		yield item