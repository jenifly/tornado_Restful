import logging

import orjson

from typing import (Union, Dict)

from handlers import ApiHandler
from tornado.escape import utf8
from tornado.util import unicode_type

from config import IMG_CODE_EXPIRES_SECONDS
from utils.captcha.captcha import captcha

class ImageCodeHandler(ApiHandler):
    route = r'/api/imgcode'

    async def get(self):
        pre_code_id = self.get_argument('pre', None)
        cur_code_id = self.get_argument('cur', None)
        if not cur_code_id:
            return self.write(4004)
        text, pic = captcha.generate_captcha()
        try:
            if pre_code_id:
                await self.redis.delete('img_code_%s' % pre_code_id)
            await self.redis.setex('img_code_%s' % cur_code_id, IMG_CODE_EXPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            self.write(4006)
        self.write_img(pic)

    async def post(self):
        code = self.json_args.get('imageCode', None)
        code_id = self.json_args.get('imageCodeId', None)
        if not code or not code_id:
            return self.write(4004)
        try:
            real_img_code = await self.redis.get('pic_code_%s' % code_id)
            await self.redis.delete('pic_code_%s' % code_id)
        except Exception as e:
            logging.error(e)
            return self.write(4001)
        if not real_img_code:
            return self.write(4600)
        if real_img_code != code.upper():
            return self.write(4601)
        self.write()

    def write_img(self, img_bytes: bytes) -> None:
        if self._finished:
            raise RuntimeError('Cannot write() after finish()')
        self.set_header('Content-Type', 'image/jpg')
        self._write_buffer.append(img_bytes)