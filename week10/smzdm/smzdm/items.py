# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SmzdmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()
    comment_id = scrapy.Field()
    comment_text = scrapy.Field()


class SmzdmGoodItem(scrapy.Item):
    goods_id = scrapy.Field()
