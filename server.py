import asyncio

import aioredis
import aiomysql

import tornado.web
import tornado.options
from functools import partial
from typing import (Any, List, Type, Dict, Awaitable)

from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

try:
    import uvloop

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
        db_pool: Dict[str, Awaitable] = None,
        **settings: Any
    ) -> None:
        if db_pool is not None:
            self.__dict__.update(db_pool)
        _handlers = []
        for handler in ApiHandler.__subclasses__():
            if hasattr(handler, 'route'):
                _handlers.append((handler.route, handler))
                del handler.route
        super().__init__(_handlers, default_host, transforms, **settings)


async def main() -> None:
    options.log_file_prefix = log_path
    options.logging = log_level
    tornado.options.parse_command_line()
    db_pool = {
        'mysql': Mysql(await aiomysql.create_pool(**mysql_options)),
        'redis': await aioredis.create_redis_pool(**redis_options)
    }
    app = RestfulApp(db_pool=db_pool, **settings)
    app.listen(options.port)


if __name__ == '__main__':
    asyncio.ensure_future(main())
    asyncio.get_event_loop().run_forever()