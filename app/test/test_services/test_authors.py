import os
import random
import unittest

import asyncpg
import asyncpg.transaction

from app.adapter.pg.session import StoragePGProvider
from app.domain.entity.authors import *
from app.domain.exc import NotFound
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.service.authors import AuthorsService


class AuthorsTest(unittest.IsolatedAsyncioTestCase):
    _tr: asyncpg.transaction.Transaction
    conn: asyncpg.Connection
    repo: AuthorsPGStorage
    use_case: AuthorsService

    base_ref = AuthorRef(
        name=random.randint(0, 100000),
        image_link=random.randint(0, 100000),
        birthdate=datetime.now(),
        death_date=datetime.now(),
    )

    @classmethod
    async def asyncSetUp(cls) -> None:
        cls.conn = await asyncpg.connect(StoragePGProvider.conf)
        cls._tr = cls.conn.transaction()
        await cls._tr.start()

        cls.repo = AuthorsPGStorage(cls.conn)
        cls.use_case = AuthorsService(cls.repo)

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
        ref_ids = [(await self.use_case.create(self.base_ref)).id for _ in range(10)]

        ls = [i.id for i in await self.use_case.list_()]

        for id_ in ref_ids:
            if id_ not in ls:
                self.fail("Ref id not in list")
