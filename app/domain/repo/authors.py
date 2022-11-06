from app.adapter.pg.repo import PGStorage
from app.domain.entity.authors import *
from app.domain.service.authors import AuthorsStorage
from . import authors_sql as sql
from ..exc import NotFound


class AuthorsPGStorage(AuthorsStorage, PGStorage):
    async def create(self, ref: AuthorRef) -> Author:
        id_ = await self._db.fetchval(
            sql.CREATE, ref.name, ref.image_link, ref.birthdate, ref.death_date
        )

        return Author(id=id_, **ref.dict())

    async def update(self, id_: int, ref: AuthorUpd):
        r = await self._db.fetchval(
            sql.UPDATE, id_, ref.name, ref.image_link, ref.birthdate, ref.death_date
        )

        if r is None:
            raise NotFound

    async def delete(self, id_: int):
        id_ = await self._db.fetchval(sql.DELETE, id_)

        if id_ is None:
            raise NotFound

    async def get(self, id_: int) -> Author:
        r = await self._db.fetchrow(sql.GET, id_)

        if r is None:
            raise NotFound

        return Author(**r)

    async def list_(self, params: AuthorFilter) -> AuthorList:
        r = await self._db.fetch(sql.LIST)
        return list(map(lambda x: Author(**x), r))
