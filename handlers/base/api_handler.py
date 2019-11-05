import hmac

import orjson

from typing import (Union, Dict)

from tornado.web import RequestHandler, HTTPError
from tornado.escape import utf8

from utils.session import Session
from utils.response_code import RESPONSE_STATUS_MAP

class ApiHandler(RequestHandler):

    @property
    def mysql(self):
        return self.application.mysql

    @property
    def redis(self):
        return self.application.redis

    def check_xsrf_cookie(self) -> None:
        token = self.get_cookie('_xsrf', None)
        if not token:
            raise HTTPError(403, "'_xsrf' argument missing from POST")
        _, token, _ = self._decode_xsrf_token(token)
        _, expected_token, _ = self._get_raw_xsrf_token()
        if not token:
            raise HTTPError(403, "'_xsrf' argument has invalid format")
        if not hmac.compare_digest(utf8(token), utf8(expected_token)):
            raise HTTPError(403, "XSRF cookie does not match POST argument")

    async def prepare(self) -> None:
        if not hasattr(self, 'seesion'):
            self.session = await Session(self).initialize()
        del self._headers['server']
        if self.request.headers.get('Content-Type', '').startswith('application/json'):
            if self.request.body:
                self.json_args = orjson.loads(self.request.body.decode())
        else:
            self.json_args = {}

    def write(
        self,
        status: int = 4000,
        data: Union[str, bytes, dict] = None
    ) -> None:
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if data:
            if not isinstance(data, dict):
                data = {'msg': data}
            data['status'] = status 
        else:
            data = {'status': status, 'msg': RESPONSE_STATUS_MAP[status]}
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self._write_buffer.append(utf8(orjson.dumps(data)))