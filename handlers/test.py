import re

from pymysql.err import InternalError

from handlers import ApiHandler

class TestHandler(ApiHandler):
    route = r'/api/test/?([^/]*)/?'

    async def get(self, name):
        if name:
            try:
                data = await self.mysql.queryone('SELECT * FROM article WHERE id={}'.format(name))
                self.write({'res': data})
            except InternalError as e:
                e = re.search(r"'(.*)' ", e.__str__())
                self.write(4004, {'msg': f'参数错误：< {e.group(1)} >'})
        else:
            self.write({'res': await self.mysql.queryall('SELECT * FROM article', cache=True)})
