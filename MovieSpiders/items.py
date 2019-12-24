# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviespidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    num = scrapy.Field()  # 编号
    name = scrapy.Field()  # 名称
    cover = scrapy.Field()  # 封面图片
    starrings = scrapy.Field()  # 主演
    type = scrapy.Field()  # 类型
    director = scrapy.Field()  # 导演
    region = scrapy.Field()  # 地区
    year = scrapy.Field()  # 年份
    language = scrapy.Field()  # 语言
    introduction = scrapy.Field()  # 简介
    state = scrapy.Field()  # 电视剧更新状态/电影清晰度
    fromUrl = scrapy.Field()  # 来源地址

# 示例如果有多个item，如何在pipelines中处理
class MovieplayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    num = scrapy.Field()  # 编号
    playLink = scrapy.Field()  # 播放地址