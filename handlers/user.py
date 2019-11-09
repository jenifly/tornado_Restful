from handlers import ApiHandler
from utils.commons import required_login


class UserHandler(ApiHandler):
    route = r'/api/user'

    @required_login
    async def get(self):
        self.write(self.current_user)

    @required_login
    async def post(self):
        pass

    @required_login
    async def update(self):
        pass

    @required_login
    async def delete(self):
        pass