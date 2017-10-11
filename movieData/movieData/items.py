# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class MovieDataLoader(ItemLoader):
    default_output_processor = TakeFirst()

class MoviedataItem(scrapy.Item):
    # define the fields for your item here like:
    etitle = scrapy.Field()
    ctitle = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    plot = scrapy.Field()
    rating = scrapy.Field()
    tags = scrapy.Field()
    recoMovies = scrapy.Field()




