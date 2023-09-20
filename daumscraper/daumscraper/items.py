# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    platform_id = scrapy.Field()
    cat1_id = scrapy.Field()
    cat2_id = scrapy.Field()
    category_url = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    sticker_url = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    sticker = scrapy.Field()
    writer = scrapy.Field()
    pass
