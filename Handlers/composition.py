import tornado.web
import json
import functools


class ChemicalCompositionHandler(tornado.web.RequestHandler):

    async def post(self):
        request_body = json.loads(self.request.body)
        if request_body:
            query = f'SELECT * FROM COMPOSITION WHERE commodity_id={request_body["commodity_id"]}'
            composition = await self.settings['sqlite'].fetch_all(query)
            total = functools.reduce(lambda x, y: x + y['percentage'], composition, 0)
            if total == 100 or (total+request_body['percentage'] > 100):
                self.finish({'message': 'Total concentration of elements exceeds 100'})
            else:
                if request_body['element_id'] not in [x['element_id'] for x in composition]:
                    sql_query = ''' INSERT INTO COMPOSITION(element_id,commodity_id,percentage)
                                  VALUES(?,?,?) '''
                    await self.settings['sqlite'].execute(sql_query,
                                                          request_body['element_id'],
                                                          request_body['commodity_id'],
                                                          request_body['percentage'])
                    self.finish({'message': 'Successfully Add composition'})
                else:
                    sql_query = ''' UPDATE COMPOSITION SET 'percentage' = ? WHERE element_id = ? AND commodity_id = ? '''
                    await self.settings['sqlite'].execute(sql_query,
                                                          request_body['percentage'],
                                                          request_body['element_id'],
                                                          request_body['commodity_id'])
                    self.finish({'message': 'Successfully update composition'})
                    # self.finish({'message': 'composition already exists'})
        else:
            self.finish({})

    async def delete(self):
        request_body = json.loads(self.request.body)
        if request_body:
            sql_query = 'DELETE FROM COMPOSITION WHERE element_id = ? AND commodity_id = ?'
            await self.settings['sqlite'].execute(sql_query,
                                                  request_body['element_id'],
                                                  request_body['commodity_id'])
            self.finish({'message': 'Successfully deleted composition'})
        else:
            self.finish({})
