# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class BooksPipeline:
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="actowiz",
            db="quotes",
            charset="utf8mb4"
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS quote_data (
                title TEXT,
                author TEXT,
                tags TEXT
            )
        """)

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO quote_data (title, author, tags)
            VALUES (%s, %s, %s)
        """, (
            item.get("title"),
            item.get("author"),
            ", ".join(item.get("tags", [])),
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
