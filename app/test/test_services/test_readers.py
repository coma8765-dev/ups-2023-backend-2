import os
import random
import unittest

import asyncpg
import asyncpg.transaction

from app.adapter.pg.session import StoragePGProvider
from app.domain.entity.readers import *
from app.domain.exc import NotFound
from app.domain.repo.readers import ReadersPGStorage
from app.domain.service.readers import ReadersService


class ReadersTest(unittest.IsolatedAsyncioTestCase):
    _tr: asyncpg.transaction.Transaction
    conn: asyncpg.Connection
    repo: ReadersPGStorage
    use_case: ReadersService

    base_ref: ReaderRef

    @property
    def base_ref(self) -> ReaderRef:
        return ReaderRef(
            name=random.randint(0, 100000), email=random.randint(0, 100000)
        )

    @classmethod
    async def asyncSetUp(cls) -> None:
        cls.conn = await asyncpg.connect(StoragePGProvider.conf)
        cls._tr = cls.conn.transaction()
        await cls._tr.start()

        cls.repo = ReadersPGStorage(cls.conn)
        cls.use_case = ReadersService(cls.repo)

    @classmethod
    async def asyncTearDown(cls) -> None:
        # Help with filling database
        if not os.getenv("TEST_NO_COMMIT", 0):
            await cls._tr.rollback()
        else:
            await cls._tr.commit()

    async def test_create(self):
        ref = self.base_ref
        r = await self.use_case.create(ref)
        self.assertDictEqual(r.dict(exclude={"id"}), ref.dict())

    async def test_delete(self):
        r = await self.use_case.create(self.base_ref)
        await self.use_case.delete(r.id)

        with self.assertRaises(NotFound):
            await self.use_case.get(r.id)

        with self.assertRaises(NotFound):
            await self.use_case.delete(r.id)
