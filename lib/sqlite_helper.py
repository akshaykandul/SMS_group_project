import sqlite3
import tornado.concurrent
import concurrent.futures
import tornado.platform.asyncio

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SQLITE(object):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    @tornado.concurrent.run_on_executor
    def _fetch_all(self, query, *args):
        if args:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    @tornado.concurrent.run_on_executor
    def _fetch_one(self, query, *args):
        if args:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    @tornado.concurrent.run_on_executor
    def _execute(self, query, *args):
        if args:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    async def fetch_all(self, query, *args):
        return await tornado.platform.asyncio.to_tornado_future(self._fetch_all(query, *args))

    async def fetch_one(self, query, *args):
        return await tornado.platform.asyncio.to_tornado_future(self._fetch_one(query, *args))

    async def execute(self, query, *args):
        return await tornado.platform.asyncio.to_tornado_future(self._execute(query, *args))

    def __del__(self):
        self.conn.close()
