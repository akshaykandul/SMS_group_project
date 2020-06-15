from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
import lib.sqlite_helper

from Handlers.elements import ChemicalElementsHandler
from Handlers.composition import ChemicalCompositionHandler
from Handlers.commodity import CommodityHandler

from tornado.options import define, options
define("port", default=8000, type=int)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    sqlite = lib.sqlite_helper.SQLITE('local.db')
    app = tornado.web.Application([
        (r"/api/v1/elements", ChemicalElementsHandler),
        (r"/api/v1/commodity", CommodityHandler),
        (r"/api/v1/composition", ChemicalCompositionHandler)
    ], ** {"sqlite": sqlite})

    app.listen(options.port)
    print(f"Web Server is listening on {options.port}")
    tornado.ioloop.IOLoop.current().start()
