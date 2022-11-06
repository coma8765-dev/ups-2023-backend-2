from app.adapter.pg.repo import PGStorage
from app.domain.entity.rentals import *
from app.domain.exc import NotFound
from app.domain.service.rentals import RentalsStorage
from . import rentals_sql as sql


class RentalsPGStorage(RentalsStorage, PGStorage):
    async def create(self, ref: RentalRef) -> Rental:
        id_ = await self._db.fetchval(
            sql.CREATE,
            ref.book_id,
            ref.reader_id,
            ref.fine_amount,
        )

        return Rental(id=id_, **ref.dict(), start=datetime.now())

    async def list_(self, params: RentalFilter) -> list[Rental]:
        r = await self._db.fetch(
            sql.LIST,
            params.book_id,
            params.reader_id,
            params.is_returned,
        )

        return [Rental(**i) for i in r]

    async def update(self, id_: int, ref: RentalUpd):
        r = await self._db.fetchval(
            sql.UPDATE,
            id_,
            ref.end,
        )

        if r is None:
            raise NotFound

    async def get_by_book_and_reader(self, reader_id: int, book_id: int) -> Rental:
        r = await self._db.fetchrow(
            sql.GET_BY_BOOK_AND_READER,
            reader_id,
            book_id,
        )

        if r is None:
            raise NotFound

        return Rental(**r)
