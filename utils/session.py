import orjson
import logging

from typing import (Type, Dict)
from config import SESSION_PREFIX, SESSION_EXPIRES_SECONDS, SEESION_HASH_KEY
from .commons import encryption

class Session(object):
    def __init__(self,
        handler: Type['ApiHandler'] = None
    ) -> None:
        self._handler = handler
        self._token = handler.get_secure_cookie('_token')

    async def initialize(self) -> None:
        if not self._token:
            self.data = None
        else:
            self._token = '{}{}'.format(SESSION_PREFIX, self._token.decode())
            try:
                json_data = await self._handler.redis.get(self._token)
            except Exception as e:
                logging.error(e)
                raise e
            if not json_data:
                self.data = None
            else:
                self.data = orjson.loads(json_data.decode())
        return self

    async def save(
        self,
        data: Dict = None
    ) -> None:
        self.data = data
        _token = encryption('{}{}'.format(self.data['username'], SEESION_HASH_KEY))
        self._token = '{}{}'.format(SESSION_PREFIX, _token)
        serialize_data = orjson.dumps(data)
        try:
            await self._handler.redis.setex(self._token, SESSION_EXPIRES_SECONDS, serialize_data)
            self._handler.set_secure_cookie('_token', _token)
        except Exception as e:
            logging.error(e)
            raise e

    async def clear(self) -> bool:
        try:
            await self._handler.redis.delete(self._token)
            self._handler.clear_cookie('_token')
            return True
        except Exception as e:
            logging.error(e)
            raise e