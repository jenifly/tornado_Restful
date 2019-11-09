import logging

from handlers import ApiHandler
from utils.commons import required_login, encryption
from config import SEESION_HASH_KEY, SESSION_PREFIX, PASSWD_HASH_KEY


class PassportHandler(ApiHandler):
    route = r'/api/passport'

    def check_xsrf_cookie(self) -> None:
        if self.request.method == 'post':
            self.xsrf_token
        else:
            super().check_xsrf_cookie()

    async def post(self):    # login
        username = self.json_args.get('username', None)
        password = self.json_args.get('password', None)
        if not username or not password:
            return self.write(4004)
        try:
            user_info = await self.mysql.queryone(f'SELECT * from user where username="{username}"')
            if not user_info:
                return self.write(4002)
            if encryption(f'{password}{PASSWD_HASH_KEY}') == user_info['password']:
                _token = f'{SESSION_PREFIX}{encryption(f"{username}{SEESION_HASH_KEY}")}'
                if await self.redis.get(_token):
                    return self.write(4103)
                del user_info['password']
                await self.session.save(user_info)
                self.write(4000)
            else:
                self.write(4101)
        except Exception as e:
            logging.error(e)
            self.write(4001)

    @required_login
    async def get(self):    # logout
        try:
            self.session.clear()
            self.write(4000)
        except Exception as e:
            self.write(4006)
            logging.error(e)
            raise e
