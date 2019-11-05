import tornado.web
import tornado.options
import aioredis
import aiomysql

from functools import partial
from typing import (Any, List, Type)

from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

try:
    import uvloop
    import asyncio

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from utils.mysql import Mysql
from handlers import ApiHandler
from config import log_path, log_level, settings, mysql_options, redis_options


define('port', type=int, default=5266)


class RestfulApp(Application):
    def __init__(self,
        default_host: str = None,
        transforms: List[Type['OutputTransform']] = None,
        **settings: Any
    ) -> None:
        _handlers = []
        for handler in ApiHandler.__subclasses__():
            if hasattr(handler, 'route'):
                _handlers.append((handler.route, handler))
                del handler.route
        super().__init__(_handlers, default_host, transforms, **settings)


async def initialize_aiodb_pool(app) -> None:
    app.mysql = Mysql(await aiomysql.create_pool(**mysql_options))
    app.redis = await aioredis.create_redis_pool(**redis_options)


def main() -> None:
    options.log_file_prefix = log_path
    options.logging = log_level
    tornado.options.parse_command_line()
    app = RestfulApp(**settings)
    app.listen(options.port)
    io_loop = IOLoop.current()
    io_loop.add_callback(partial(initialize_aiodb_pool, app))
    io_loop.start()


if __name__ == '__main__':
    main()
