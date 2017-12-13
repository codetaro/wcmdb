import datetime
import pytz
import scrapy

from wcmdb.items import WcmdbItem


class SmhSpider(scrapy.Spider):
    name = "smh"
    local_tz = pytz.timezone("Australia/Sydney")

    def start_requests(self):
        urls = [
            "http://www.smh.com.au/nsw",
            "http://www.smh.com.au/national",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.xpath('//div[@class="grid"]/article'):
            href = article.xpath('./div/h3/a/@href').extract_first()
            yield scrapy.Request(href, callback=self.parse_article)

    def parse_article(self, response):
        item = WcmdbItem()
        item['title'] = response.xpath('//header[@class="article__header"]/h1/text()').extract_first().strip()
        item['keywords'] = response.xpath('//meta[@name="keywords"]/@content').extract_first().split(", ")
        item['author'] = response.xpath('//h5[@rel="author"]/text()').extract_first()
        item['category'] = response.url.split("/")[3]
        sydney_time = datetime.datetime.strptime(
            response.xpath('///time[@class="signature__datetime"]/@datetime').extract_first()[:-5],
            "%Y-%m-%dT%H:%M:%S")
        item['add_time'] = self.local_tz.localize(sydney_time, is_dst=None).astimezone(pytz.utc)
        item['scrape_time'] = datetime.datetime.utcnow().replace(microsecond=0)
        yield item
