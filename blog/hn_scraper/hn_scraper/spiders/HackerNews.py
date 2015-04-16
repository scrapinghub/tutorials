# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from hn_scraper.items import HnArticleItem


class HackernewsSpider(Spider):
    name = "HackerNews"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ('https://news.ycombinator.com/', )

    link_extractor = SgmlLinkExtractor(
        allow=('news', ),
        restrict_xpaths=('//a[text()="More"]', ))

    def extract_one(self, selector, xpath, default=None):
        extracted = selector.xpath(xpath).extract()
        if extracted:
            return extracted[0]
        return default

    def parse(self, response):
        for link in self.link_extractor.extract_links(response):
            request = Request(url=link.url)
            request.meta.update(link_text=link.text)
            yield request

        for item in self.parse_item(response):
            yield item

    def parse_item(self, response):
        selector = Selector(response)

        rows = selector.xpath('//table[@id="hnmain"]//td[count(table) = 1]' \
                              '//table[count(tr) > 1]//tr[count(td) = 3]')
        for row in rows:
            item = HnArticleItem()

            article = row.xpath('td[@class="title" and count(a) = 1]//a')
            article_url = self.extract_one(article, './@href', '')
            article_title = self.extract_one(article, './text()', '')
            item['url'] = article_url
            item['title'] = article_title

            subtext = row.xpath(
                './following-sibling::tr[1]//td[@class="subtext" and count(a) = 3]')
            if subtext:
                item_author = self.extract_one(subtext, './/a[1]/@href', '')
                item_id = self.extract_one(subtext, './/a[2]/@href', '')
                item['author'] = item_author[8:]
                item['id'] = int(item_id[8:])

            yield item
