# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import json
import traceback
import pymysql
from snownlp import SnowNLP
from smzdm import config
from smzdm.items import SmzdmItem, SmzdmGoodItem


class SmzdmPipeline:
    """
    数据处理、新增和删除
    """

    def __init__(self, host, port, database, table, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.good_table, self.comment_table, self.analysis = table
        self.user = user
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            database=config.MYSQL_DBNAME,
            table=config.MYSQL_TABLE,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWD
        )

    def open_spider(self, spider):
        self.new_goods = []
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        cursor = self.db.cursor()
        if isinstance(item, SmzdmGoodItem):
            self.new_goods = item['goods_id']
            return item

        # 更新goods表
        sql = f"""INSERT IGNORE INTO {self.good_table} (good_id, good_name) VALUES ("{item['goods_id']}", "{item['good_name']}")"""
        try:
            cursor.execute(sql)
            self.db.commit()
            print("Update goods success")
        except Exception:
            traceback.print_exc()
            self.db.rollback()

        # 更新origin_comments表
        sql = f"""INSERT IGNORE INTO {self.comment_table} (comm_id, content, good_id) VALUES ("{item['comment_id']}", "{item['comment_text']}", "{item['goods_id']}")"""
        try:
            cursor.execute(sql)
            self.db.commit()
            print("Update original comment table success")
        except Exception:
            traceback.print_exc()
            self.db.rollback()

        # 评论语义分析
        if item["comment_text"] != "":
            s = SnowNLP(item['comment_text'])
            sentiment = s.sentiments
            sql = f"""INSERT IGNORE INTO {self.analysis} (comm_id, content, sentiments, good_id) VALUES ("{item['comment_id']}", "{item['comment_text']}", "{sentiment}", "{item['goods_id']}")"""
            try:
                cursor.execute(sql)
                self.db.commit()
                print("Update opinion analysis table success")
            except Exception:
                traceback.print_exc()
                self.db.rollback()

        if self.new_goods != []:
            sql = f"""SELECT * FROM {self.good_table}"""
            try:
                cursor.execute(sql)
                self.db.commit()
            except Exception:
                traceback.print_exc()
                self.db.rollback()

            result = cursor.fetchall()
            to_delete = [(d[0]) for d in result if d[0] not in self.new_goods]
            if to_delete != []:
                sql = f"""DELETE FROM {self.good_table} WHERE good_id=(%s)"""
                try:
                    cursor.executemany(sql, to_delete)
                    self.db.commit()
                    print("Delete old goods success")
                except Exception:
                    traceback.print_exc()
                    self.db.rollback()
        return item
