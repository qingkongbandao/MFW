# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MfwItem(scrapy.Item):
    subTitle = scrapy.Field()
    cityUrl = scrapy.Field()
    subFilename = scrapy.Field()
    parentNames = scrapy.Field()
    parentPages = scrapy.Field()
    titleURL = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    # morePage = scrapy.Field()
    tag_filename = scrapy.Field()
    title_desc = scrapy.Field()  # 标题描述


class MfwItemMore(scrapy.Item):
    subTitle = scrapy.Field()
    cityUrl = scrapy.Field()
    subFilename = scrapy.Field()
    parentNames = scrapy.Field()
    parentPages = scrapy.Field()
    titleURL = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag_filename = scrapy.Field()
    title_desc = scrapy.Field()


class MfwItemTag(scrapy.Item):
    subTitle = scrapy.Field()
    cityUrl = scrapy.Field()
    subFilename = scrapy.Field()
    parentNames = scrapy.Field()
    parentPages = scrapy.Field()
    titleURL = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag_title_dir = scrapy.Field()




