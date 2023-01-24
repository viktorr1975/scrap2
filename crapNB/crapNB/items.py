# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComputerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    cpu = scrapy.Field()
    ram = scrapy.Field()
    ssd = scrapy.Field()
    price = scrapy.Field()
    rank = scrapy.Field()

