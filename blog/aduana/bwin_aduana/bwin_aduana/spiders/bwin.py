# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

from bwin_aduana.items import PlayerItem, EventItem

class BwinSpider(scrapy.Spider):
    name = "bwin"
    allowed_domains = ["bwin.com", "sports.bwin.com"]

    def start_requests(self):
        return [ FormRequest('https://sports.bwin.com/en/sports/indexmultileague',
               formdata={ 'sportId': '5', 'page': '1' },
                callback=self.parse) ]

    def get_players(self, text):
        players = []
        for td in text.css('table.options td'):
            player = PlayerItem()
            player['odds'] = td.css('.odds::text').extract_first()
            player['name'] = td.css('.option-name::text').extract_first()
            players.append(player)
        return players

    def get_events(self, text):
        events = []
        league = text.xpath('h2//a[@class="league-link"]/text()').extract()
        for li in text.css('ul li'):
            event = EventItem()
            event['time'] = li.xpath('h6//span[1]/text()').extract_first()
            event['date'] = li.xpath('h6//span[2]/text()').extract_first()
            event['players'] = self.get_players(li)
            events.append(event)
        return events        

    def parse(self, response):
        leagues = response.xpath('//div[@id="bet-offer"]//div[@id="international-highlights"]//div//ul//li')
        events = []
        for league in leagues:
            events.extend(self.get_events(league))
        
        return events
