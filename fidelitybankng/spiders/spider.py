import scrapy

from scrapy.loader import ItemLoader

from ..items import FidelitybankngItem
from itemloaders.processors import TakeFirst


class FidelitybankngSpider(scrapy.Spider):
	name = 'fidelitybankng'
	start_urls = ['https://www.fidelitybank.ng/media-centre/blog/']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "elementor-element-57e8ebb", " " ))]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="page-numbers next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1//text()').get()
		description = response.xpath('//div[contains(@class,"elementor-widget-theme-post-content")]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//meta[@property="article:published_time"]/@content').get()

		item = ItemLoader(item=FidelitybankngItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
