# -*- coding: utf-8 -*-
import re

import execjs
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from MovieSpiders.items import MoviespidersItem, MovieplayItem

"""
    Scrapy框架中分两类爬虫,Spider类和CrawlSpider类。
    crawlspider是Spider的派生类(一个子类)，Spider类的设计原则是只爬取start_url列表中的网页，
    而CrawlSpider类定义了一些规则(rule)来提供跟进link的方便的机制，从爬取的网页中获取link并继续爬取的工作更适合。
    CrawlSpider类和Spider类的最大不同是CrawlSpider多了一个rules属性，其作用是定义”提取动作“。在rules中可以包含一个或多个Rule对象，在Rule对象中包含了LinkExtractor对象。
"""


class XiaoshoumoviesSpider(CrawlSpider):
    """
       name:scrapy唯一定位实例的属性，必须唯一
       allowed_domains：允许爬取的域名列表，不设置表示允许爬取所有
       start_urls：起始爬取列表
       start_requests：它就是从start_urls中读取链接，然后使用make_requests_from_url生成Request，
                       这就意味我们可以在start_requests方法中根据我们自己的需求往start_urls中写入
                       我们自定义的规律的链接
       parse：回调函数，处理response并返回处理后的数据和需要跟进的url
       log：打印日志信息
       closed：关闭spider
     """
    name = 'XiaoShouMovies'
    allowed_domains = ['www.p4vip.com']
    start_urls = ['http://www.p4vip.com/?m=vod-type-id-1.html', 'http://www.p4vip.com/?m=vod-type-id-2.html',
                  'http://www.p4vip.com/?m=vod-type-id-3.html', 'http://www.p4vip.com/?m=vod-type-id-4.html',
                  'http://www.p4vip.com/?m=vod-type-id-16.html']

    # 连接提取器：会去起始url响应回来的页面中提取指定的url
    # rules元组中存放的是不同的规则解析器（封装好了某种解析规则)
    rules = (
        # 规则解析器：可以将连接提取器提取到的所有连接表示的页面进行指定规则（回调函数）的解析
        # Rule(LinkExtractor(allow=r'.*type-id-8-.*'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[text()="下一页"]'), follow=True),
        # Rule(LinkExtractor(allow=r'.*detail-id-\d{1,8}\.html'),callback='parse_list',  follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="link-hover"]'), callback='parse_list', follow=True),
        # 由于该网站所有的播放链接都是存在一起的，即在任何一个剧集播放页面即可拿到全集的播放地址链接。所以单独爬取一个页面即可，不需要爬取全部页面链接
        Rule(LinkExtractor(allow='.*play-id-\d{1,8}-src-1-num-1.html'), callback='parse_link', follow=False),
    )

    # 解析列表页方法
    def parse_list(self, response):
        # # 根据xpath表达式提取电影各种信息
        # for a in a_list:
        #     item = MovieByXiaoShouItem()
        #     item['movie_name'] = a.xpath('@title').get()
        #     item['movie_cover'] = a.xpath('./img/@data-original').get()
        #     yield item
        # print(response.xpath('//dt[@class="name"]/text()').get())
        item = MoviespidersItem()
        try:
            # item['num'] = re.findall('(?<=detail-id-).*(?=\.html)',response.request.url)[0]
            item['num'] = re.findall(r'\d{1,8}', response.request.url)[1]
            item['name'] = response.xpath('//dt[@class="name"]/text()').get()
            item['cover'] = response.xpath('//img[@class="lazy"]/@data-original').get()
            starrings = response.xpath('//dt[2]/a/text()')
            starring_arr = []
            for starring in starrings:
                starring_arr.append(starring.get())
            item['starrings'] = ','.join(starring_arr)
            item['type'] = response.xpath('//dt[3]/a/text()').get()
            item['director'] = response.xpath('//dd[1]/a/text()').get()
            item['region'] = response.xpath('//dd[1]/dd/text()').get()
            item['year'] = response.xpath('//dd[2]/text()').get()
            item['language'] = response.xpath('//dd[3]/text()').get()
            introduction = response.xpath('//div[@class="tab-jq"]/span/text()').get()
            if introduction is None:
                introduction = response.xpath('//div[@class="tab-jq"]/text()').get().strip()
            item['introduction'] = introduction
            item['state'] = response.xpath('//span[@class="bz"]/text()').get()
            item['fromUrl'] = response.request.url
        except Exception:
            with open('./exception.txt', 'w') as f:
                f.write(response.xpath('//dt[@class="name"]/text()').get() + '   ---   ' + response.request.url + '\n')
                f.close()
        return item

    # 解析播放页的播放地址
    def parse_link(self, response):
        item = MovieplayItem()
        try:
            item['num'] = re.findall(r'\d{1,8}', response.request.url)[1]
            playLink = re.findall(r'(?<=mac_url\=unescape\(\').*?(?=\'\))', response.text)[0]
            link = execjs.eval("unescape('" + playLink + "')")
            item['playLink'] = link
        except Exception:
            with open('./exception.txt', 'w') as f:
                f.write(
                    response.xpath('//dt[@class="name"]/text()').get() + '   -url-   ' + response.request.url + '\n')
                f.close()
        return item
