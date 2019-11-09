import functools
import logging
import hashlib
import os

from typing import Type
from tornado.escape import utf8

from config import ufiles_path

def required_login(fun):
    @functools.wraps(fun)
    async def wrapper(handler: Type['ApiHandler'] = None, *args, **kwargs):
        if handler.current_user:
            await fun(handler, *args, **kwargs)
        else:
            handler.write(4102)
    return wrapper


def encryption(context: str = None) -> bytes:
    return hashlib.sha256(utf8(context)).hexdigest()
