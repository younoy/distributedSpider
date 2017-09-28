# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from scrapy.exporters import JsonItemExporter

class ArticlebolePipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_close(self,spider):
        self.file.close()

class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleExporter.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def spider_close(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

class ArticleboleImagePipeline(ImagesPipeline):
    def item_completed(self,results,item,info):
        if 'front_image_url' in item:
            for ok,value in results:
                image_file = value['path']
            item['front_image_path'] = image_file
        return item

# 采用同步的机制
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            'localhost','root','root','jobBole',charset='utf8',use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = """
            INSERT INTO article(title,time,url,url_object_id)
            VALUE (%s,%s,%s,%s)
        """

        self.cursor.execute(insert_sql,(item['title'],item['time'],item['url'],item['url_object_id']))
        self.conn.commit()
        return item

# 采用异步的机制
class MysqlTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        params = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**params)
        return cls(dbpool)

    def process_item(self,item,spider):

        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        print(failure)


    def do_insert(self,cursor,item):

        insert_sql = """
            Insert INTO article(title,time,url,url_object_id,front_image_url,front_image_path,agree_num,fav_num,comment_num,content)
            VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(insert_sql,(item['title'],item['time'],item['url'],item['url_object_id'],item['front_image_url'],
                                        item['front_image_path'],item['agree_num'],item['fav_num'],item['comment_num'],item['content']))

