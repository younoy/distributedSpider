# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class MoviedataPipeline(object):
    def process_item(self, item, spider):
        return item

# 采用同步的机制
class MysqlPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(
            'localhost','root','root','movieData',charset='utf8',use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = """
            INSERT INTO movies(title,image_url,url,plot,rating,tags,recoMovies) VALUE (%s,%s,%s,%s,%s,%s,%s)
        """

        self.cursor.execute(insert_sql,(item['title'],item['image_url'],item['url'],item['plot'],item['rating'],
                                        item['tags'],item['recoMovies']))
        self.conn.commit()
        return item

