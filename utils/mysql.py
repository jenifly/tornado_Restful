import logging
import re

from typing import Type, Union, Dict, List, Any, Tuple

from aiomysql import Cursor, DictCursor

from utils.cache import cache as _cache

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
        cursorclass: Type['Cursor'] = Cursor,
        cache: bool = False,
        single: bool = False
    ) -> Any:
        if cache:
            _hash = str(hash(sql))
            if not hasattr(_cache, _hash):
                cur = await self.execute(sql, cursorclass)
                tmp = await cur.fetchone() if single else await cur.fetchall()
                setattr(_cache, _hash, tmp)
            return getattr(_cache, _hash)
        else:
            cur = await self.execute(sql, cursorclass)
            return await cur.fetchone() if single else await cur.fetchall()

    async def insert(
        self,
        table: str = None,
        column: str = None,
        value: Union[str, Tuple] = None
    ) -> Any:
        if isinstance(value, tuple):
            value = '),('.join(value)
        cur = await self.execute(f'INSERT INTO {table} ({column}) VALUES ({value})')
        return cur.lastrowid, cur.rowcount

    async def update(
        self,
        sql: str = None,
    ) -> Any:
        cur = await self.execute(sql)
        return cur.rowcount

    async def delete(
        self,
        sql: str = None,
    ) -> Any:
        cur = await self.execute(sql)
        return cur.rowcount

    async def execute(
        self,
        sql: str = None,
        cursorclass: Type['Cursor'] = Cursor,
    ) -> Type['Cursor']:
        async with self._mysql_pool.acquire() as conn:
            async with conn.cursor(cursorclass) as cur:
                await cur.execute(sql)
                return cur

    async def transaction(
        self,
        sqls: Tuple = None,
    ) -> None:
        async with self._mysql_pool.acquire() as conn:
            await conn.begin()
            try:
                async with conn.cursor() as cur:
                    for sql in sqls:
                        await cur.execute(sql)
            except Exception as e:
                await conn.rollback()
                raise e
            else:
                await conn.commit()