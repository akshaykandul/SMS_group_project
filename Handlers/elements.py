import tornado.web
import json


class ChemicalElementsHandler(tornado.web.RequestHandler):

    async def get(self):
        query = "SELECT * FROM Elements"
        records = await self.settings['sqlite'].fetch_all(query)
        self.finish(json.dumps(records))
