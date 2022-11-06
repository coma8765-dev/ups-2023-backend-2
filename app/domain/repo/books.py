from app.adapter.pg.repo import PGStorage
from app.domain.entity.books import *
from app.domain.service.books import BooksStorage
from . import books_sql as sql
from ..exc import NotFound


class BooksPGStorage(BooksStorage, PGStorage):
    async def create(self, ref: BookRef) -> Book:
        id_ = await self._db.fetchval(
            sql.CREATE,
            ref.title,
            ref.rental_limit,
            ref.image_link,
            ref.author_id,
        )

        return Book(id=id_, **ref.dict())

    async def update(self, id_: int, ref: BookUpd):
        r = await self._db.fetchval(
            sql.UPDATE, id_, ref.title, ref.rental_limit, ref.image_link,
            ref.author_id
        )

        if r is None:
            raise NotFound

    async def delete(self, id_: int):
        id_ = await self._db.fetchval(sql.DELETE, id_)

        if id_ is None:
            raise NotFound

    async def get(self, id_: int) -> Book:
        r = await self._db.fetchrow(sql.GET, id_)

        if r is None:
            raise NotFound

        return Book(**r)

    async def list_(self, params: BookFilter) -> BookList:
        r = await self._db.fetch(
            sql.LIST,
            params.author_id,
            params.title,
            params.is_available,
        )
        return list(map(lambda x: Book(**x), r))
