import os
import random
import unittest
from datetime import datetime, timedelta

import asyncpg
import asyncpg.transaction

from app.adapter.pg.session import StoragePGProvider
from app.domain.entity.authors import AuthorRef
from app.domain.entity.books import BookRef
from app.domain.entity.readers import *
from app.domain.entity.rentals import RentalFilter, RentalRef
from app.domain.exc import NotFound
from app.domain.repo.readers import ReadersPGStorage
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.repo.books import BooksPGStorage
from app.domain.repo.rentals import RentalsPGStorage
from app.domain.service.rentals import RentalsService


class ReadersTest(unittest.IsolatedAsyncioTestCase):
    _tr: asyncpg.transaction.Transaction
    conn: asyncpg.Connection
    repo: RentalsPGStorage
    use_case: RentalsService

    @classmethod
    async def asyncSetUp(cls) -> None:
        cls.conn = await asyncpg.connect(StoragePGProvider.conf)
        cls._tr = cls.conn.transaction()
        await cls._tr.start()

        cls.repo = RentalsPGStorage(cls.conn)
        cls.use_case = RentalsService(cls.repo)

        reader = await ReadersPGStorage(cls.conn).create(
            ReaderRef(name=random.randint(0, 100000), email=random.randint(0, 100000))
        )

        author = await AuthorsPGStorage(cls.conn).create(
            AuthorRef(
                name=random.randint(0, 100000),
                image_link=random.randint(0, 100000),
                birthdate=datetime.now(),
                death_date=datetime.now(),
            )
        )

        book = await BooksPGStorage(cls.conn).create(
            BookRef(
                title=random.randint(0, 100000),
                rental_limit=timedelta(days=random.randint(1, 10000)),
                image_link=random.randint(0, 10000),
                author_id=author.id,
            )
        )

        cls.rental_ref = RentalRef(
            book_id=book.id,
            reader_id=reader.id,
        )

    @classmethod
    async def asyncTearDown(cls) -> None:
        # Help with filling database
        if not os.getenv("TEST_NO_COMMIT", 0):
            await cls._tr.rollback()
        else:
            await cls._tr.commit()

    async def test_create(self):
        r = await self.repo.create(self.rental_ref)
        self.assertDictEqual(
            r.dict(include=self.rental_ref.__fields__.keys()), self.rental_ref.dict()
        )

        self.assertEqual(r.rental_time, None)

        await self.use_case.return_(self.rental_ref)
        r2 = await self.repo.get_by_book_and_reader(
            reader_id=self.rental_ref.reader_id,
            book_id=self.rental_ref.book_id,
        )

        self.assertNotEqual(r2.rental_time, None)

    async def test_list(self):
        refs = [(await self.repo.create(self.rental_ref)).id
                for _ in range(5)]

        ls = await self.repo.list_(RentalFilter(
            **self.rental_ref.dict(),
            is_returned=False,
        ))

        self.assertListEqual([i.id for i in ls], refs)
