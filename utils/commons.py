import functools
import logging
import hashlib
import os

from config import ufiles_path

def required_login(fun):
    @functools.wraps(fun)
    async def wrapper(request_handler_obj, *args, **kwargs):
        if request_handler_obj.current_user:
            await fun(request_handler_obj, *args, **kwargs)
        else:
            request_handler_obj.write(res_msg(4102))
    return wrapper

# def upload_flie(self):
#     try:
#         file_metas = self.request.files.get('file', None)
#         if not file_metas:
#             self.write(dict(msgcode=0))
#             return
#         for meta in file_metas:
#             filename = meta['filename']
#             file_path = os.path.join(ufiles_path, filename)
#             with open(file_path, 'wb') as up:
#                 up.write(meta['body'])
#             return self.write(dict(msgcode=1))
#     except:
#         return self.write(dict(msgcode=0))

def dict_sql(d):
    s = ''
    for k,v in d.items():
        s += k + '="' + str(v) + '",'
    return s[0:-1]

def encryption(context: str) -> bytes:
    return hashlib.sha256(context.encode('utf8')).hexdigest()
















