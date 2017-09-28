# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst
from scrapy.loader import ItemLoader
import datetime
import re

def dateConvert(value):
    value = value.strip().replace('·', '').strip()
    try:
        time = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        time = datetime.datetime.now().date()
    return time

def regExtrNum(value):
    match_re = re.match(r".*?(\d+).*", value)
    if match_re:
        num = int(match_re.group(1))
    else:
        num = 0
    return num

def urlValue(value):
    return value

class ArticleboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):

    title = scrapy.Field()
    time = scrapy.Field(
        input_processor=MapCompose(dateConvert),
    )

    url = scrapy.Field()
    url_object_id = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor = MapCompose(urlValue)
    )
    front_image_path = scrapy.Field()

    agree_num = scrapy.Field(
        input_processor=MapCompose(lambda x:int(x)),
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(regExtrNum),
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(regExtrNum),
    )

    content = scrapy.Field()
