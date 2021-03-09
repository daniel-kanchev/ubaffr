import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from ubaffr.items import Article


class UbaffrSpider(scrapy.Spider):
    name = 'ubaffr'
    start_urls = ['https://www.ubaf.fr/actualites']

    def parse(self, response):
        links = response.xpath('//div[@class="all-block-link"]/a[text()="Lire la suite"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('(//span[@class="field-content"])[3]//text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="block-region-bottom"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
