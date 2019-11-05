# 一个基于tornado的Restful微服务基础框架
### 环境要求：python 3.5+， tornado 6.x
1. 集成异步mysql连接池`aiomysql`、异步redis连接池`aioredis`、异步文件流库`aiofiles`，充分发挥tornado异步特性
2. 可插拔式路由:
    - 继承`handlers.ApiHandler`，添加`route`类属性
    - 在`handlers`文件夹下的`__init__.py`文件中导入继承的类

    即可完成路由解析
    #### example:
    ```python
    from handlers import ApiHandler

    class TestHandler(ApiHandler):
        route = r'/test/?([^/]*)/?'

        async def get(self, name):
            self.write('this is a test!, name: {}'.format(name))
    ```
    `__init__.py`:
    ```python
    from .test_handler import TestHandler
    ```
    浏览器访问`http://localhost:xxxx/test`或`http://localhost:xxxx/test/myname`
3. 集成基于异步`redis`连接池的`session`
4. 集成验证码：`http://localhost:xxxx/imgcode?cur=xxxxxxxxxxxxxxxxxxxxx`
5. 优化`xsrf_cookies`校验规则
6. 规范`Restful`接口