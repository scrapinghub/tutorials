# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class PlayerItem(Item):
    name = Field()
    odds = Field()

def serialize_players(players):
    return map(lambda x: dict(x), players)

class EventItem(Item):
    league = Field()
    time = Field()
    date = Field()
    players = Field(serializer=serialize_players)
