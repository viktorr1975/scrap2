# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class SimpleSqlitePipeline:

    def __init__(self):
#       conn = sqlite3.connect(:memory:)    #БД в памяти создаётся
        self.con = sqlite3.connect('computers.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            name TEXT,
            cpu TEXT,
            ram TEXT,
            ssd TEXT,
            price TEXT,
            rank REAL
        );
        """)
        self.con.commit()
        self.cur.execute("DELETE FROM computers;")
        self.con.commit()


    def process_item(self, item, spider):
        if item is not None:    #если в парсинге попались пустые строки
            self.cur.execute("""
            INSERT INTO computers (url, name, cpu, ram, ssd, price, rank) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
            item['url'],
            item['name'],
            item['cpu'],
            item['ram'],
            item['ssd'],
            item['price'],
            item['rank'],
            ))
            self.con.commit()
        return item


