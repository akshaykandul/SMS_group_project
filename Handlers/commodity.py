import tornado.web
import json

class CommodityHandler(tornado.web.RequestHandler):

    async def get_composition(self, commodity_id):
        query = f"SELECT * FROM COMPOSITION WHERE commodity_id={commodity_id}"
        composition = await self.settings['sqlite'].fetch_all(query)

        total = 0
        for element in composition:
            total += element['percentage']
            query = f'SELECT * FROM Elements WHERE id={element["element_id"]}'
            element['element'] = await self.settings['sqlite'].fetch_one(query)
            del element['element_id'], element['commodity_id']
        if total < 100:
            composition.append({
                "element": {"id": 9999, "name": "Unknown"},
                "percentage": 100 - total
            })
        return composition

    async def get(self):
        commodity_id = int(self.get_query_argument('id'))
        query = f"SELECT * FROM COMMODITY WHERE id={commodity_id}"
        records = await self.settings['sqlite'].fetch_one(query)
        if records:
            records['chemical_composition'] = await self.get_composition(commodity_id)
            self.finish(json.dumps(records))
        else:
            self.finish('Wrong Commodity Id')

    async def patch(self):
        request_body = json.loads(self.request.body)
        if request_body:
            commodity_id = str(request_body.pop('id'))
            keys = request_body.keys()
            values = request_body.values()

            query = "UPDATE COMMODITY SET '" + "' = ? ,'".join(keys) + "' = ? " + "WHERE id = " + commodity_id
            await self.settings['sqlite'].execute(query, *list(values))
            self.finish({'status': 'update successful'})
        else:
            self.finish({})
