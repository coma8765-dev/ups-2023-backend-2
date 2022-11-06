from app.adapter.pg.repo import PGStorage
from app.domain.entity.readers import *
from app.domain.service.readers import ReadersStorage
from . import readers_sql as sql
from ..exc import NotFound


class ReadersPGStorage(ReadersStorage, PGStorage):
    async def create(self, ref: ReaderRef) -> Reader:
        id_ = await self._db.fetchval(
            sql.CREATE,
            ref.name,
            ref.email,
        )

        return Reader(id=id_, **ref.dict())

    async def update(self, id_: int, ref: ReaderUpd):
        r = await self._db.fetchval(sql.UPDATE, id_, ref.name, ref.email)

        if r is None:
            raise NotFound

    async def delete(self, id_: int):
        id_ = await self._db.fetchval(sql.DELETE, id_)

        if id_ is None:
            raise NotFound

    async def get(self, id_: int) -> Reader:
        r = await self._db.fetchrow(sql.GET, id_)

        if r is None:
            raise NotFound

        return Reader(**r)
