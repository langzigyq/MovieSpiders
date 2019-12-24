# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import pymysql

from MovieSpiders.items import MoviespidersItem, MovieplayItem


class MoviespidersPipeline(object):
    def __init__(self):
        # 可选实现，做参数初始化等
        self.fp = None
        # 初始化数据库连接
        self.connect = pymysql.connect(
            db='cinema',
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            charset='utf8',
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def open_spider(self, spider):
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。
        start_time = datetime.now()
        print('开始爬虫: ' + start_time.strftime('%Y-%m-%d %H:%M:%S'))
        # self.fp = open('./data2.txt', 'w')

    def process_item(self, item, spider):
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。

        # 将爬虫文件提交的item写入数据库进行持久化存储
        # self.fp.write(item['name'] + ' ---  ' + item['fromUrl'] + '\n')
        if isinstance(item, MoviespidersItem):
            sql = 'insert into movie_detail(id,name,cover,starrings,type,director,region,year,language,introduction,state,fromUrl,update_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            lis = (
                item['num'], item['name'], item['cover'], item['starrings'], item['type'], item['director'],
                item['region'],
                item['year'], item['language'], item['introduction'], item['state'], item['fromUrl'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.cursor.execute(sql, lis)
            self.connect.commit()
        elif isinstance(item, MovieplayItem):
            # 如果有多个item，需要以此方式做处理
            sql = 'update movie_detail set playLink = %s,update_time = %s where id = %s'
            lis = (item['playLink'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), item['num'])
            self.cursor.execute(sql, lis)
            self.connect.commit()
        return item

    def close_spider(self, spider):
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        end_time = datetime.now()
        print('结束爬虫: ' + end_time.strftime('%Y-%m-%d %H:%M:%S'))
        # 关闭数据库连接
        self.connect.close()
        self.cursor.close()

        # self.fp.close()