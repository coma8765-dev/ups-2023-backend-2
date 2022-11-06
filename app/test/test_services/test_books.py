import os
import random
import unittest
from datetime import datetime

import asyncpg
import asyncpg.transaction

from app.adapter.pg.session import StoragePGProvider
from app.domain.entity.authors import AuthorRef
from app.domain.entity.books import *
from app.domain.exc import NotFound
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.repo.books import BooksPGStorage
from app.domain.service.books import BooksService


class BooksTest(unittest.IsolatedAsyncioTestCase):
    _tr: asyncpg.transaction.Transaction
    conn: asyncpg.Connection
    repo: BooksPGStorage
    use_case: BooksService

    base_ref: BookRef

    @classmethod
    async def asyncSetUp(cls) -> None:
        cls.conn = await asyncpg.connect(StoragePGProvider.conf)
        cls._tr = cls.conn.transaction()
        await cls._tr.start()

        cls.repo = BooksPGStorage(cls.conn)
        cls.use_case = BooksService(cls.repo)
        authors_storage = AuthorsPGStorage(cls.conn)
        author = await authors_storage.create(
            AuthorRef(
                name=random.randint(0, 100000),
                image_link=random.randint(0, 100000),
                birthdate=datetime.now(),
                death_date=datetime.now(),
            )
        )

        cls.base_ref = BookRef(
            title=random.randint(0, 100000),
            rental_limit=timedelta(days=random.randint(1, 10000)),
            image_link=random.randint(0, 10000),
            author_id=author.id,
        )

    @classmethod
    async def asyncTearDown(cls) -> None:
        # Help with filling database
        if not os.getenv("TEST_NO_COMMIT", 0):
            await cls._tr.rollback()
        else:
            await cls._tr.commit()

    async def test_create(self):
        r = await self.use_case.create(self.base_ref)
        self.assertDictEqual(r.dict(exclude={"id"}), self.base_ref.dict())

    async def test_delete(self):
        r = await self.use_case.create(self.base_ref)
        await self.use_case.delete(r.id)

        with self.assertRaises(NotFound):
            await self.use_case.get(r.id)

        with self.assertRaises(NotFound):
            await self.use_case.delete(r.id)

    async def test_list(self):
        ref = self.base_ref

        ref_ids = [(await self.use_case.create(ref)).id
                   for _ in range(10)]

        ls = [i.id for i in await self.use_case.list_(BookFilter(
            author_id=ref.author_id,
            title=ref.title,
            is_available=True,
        ))]

        self.assertListEqual(ls, ref_ids)
