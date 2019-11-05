import logging
import re

from typing import Type, Union, Dict, List, Any

from aiomysql import DictCursor

from utils.cache import cache

class Mysql:
    def __init__(
        self,
        mysql_pool: Type['_PoolContextManager'] = None
    ) -> None:
        self._mysql_pool = mysql_pool

    async def queryone(
        self,
        sql: str = None,
        cursorclass: Type['Cursor'] = DictCursor,
        cache: bool = False
    ) -> Union[Dict, List[str]]:
        return await self._query(sql, cursorclass, cache, True)

    async def queryall(
        self,
        sql: str = None,
        cursorclass: Type['Cursor'] = DictCursor,
        cache: bool = False
    ) -> Union[List[str], List[Dict]]:
        return await self._query(sql, cursorclass, cache)

    async def _query(
        self,
        sql: str = None,
        cursorclass: Type['Cursor'] = DictCursor,
        cache: bool = False,
        single: bool = False
    ) -> Any:
        if cache:
            _hash = str(hash(sql))
            if not hasattr(cache, _hash):
                cur = await self.execute(sql, cursorclass, False)
                tmp = await cur.fetchone() if single else await cur.fetchall()
                setattr(cache, _hash, tmp)
            return getattr(cache, _hash)
        else:
            cur = await self.execute(sql, cursorclass, False)
            return await cur.fetchone() if single else await cur.fetchall()

    async def execute(
        self,
        sql: str = None,
        cursorclass: Type['Cursor'] = DictCursor,
        commit: bool = True
    ) -> Type['Cursor']:
        commit = 'SELECT' == sql[:6].upper()
        return await self._execute(sql, cursorclass, commit)

    async def _execute(
        self,
        sql: str = None,
        cursorclass: Type['Cursor'] = DictCursor,
        commit: bool = True
    ) -> Type['Cursor']:
        async with self._mysql_pool.acquire() as conn:
            async with conn.cursor(cursorclass) as cur:
                try:
                    await cur.execute(sql)
                    return cur
                except Exception as e:
                    raise e
                finally:
                    if commit:
                        await conn.commit()
