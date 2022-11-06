from abc import ABC, abstractmethod

from fastapi import Depends

from app.domain.entity.authors import *


class AuthorsStorage(ABC):
    @abstractmethod
    async def create(self, ref: AuthorRef) -> Author:
        ...

    @abstractmethod
    async def update(self, id_: int, ref: AuthorUpd):
        ...

    @abstractmethod
    async def delete(self, id_: int):
        ...

    @abstractmethod
    async def get(self, id_: int) -> Author:
        ...

    @abstractmethod
    async def list_(self, params: AuthorFilter) -> AuthorList:
        ...


class AuthorsService:
    __slots__ = ("repo",)
    repo: AuthorsStorage

    def __init__(self, repo: AuthorsStorage = Depends()):
        self.repo = repo

    async def create(self, ref: AuthorRef) -> Author:
        return await self.repo.create(ref)

    async def update(self, id_: int, upd: AuthorUpd):
        await self.repo.update(id_, upd)

    async def get(self, id_: int) -> Author:
        return await self.repo.get(id_)

    async def delete(self, id_: int):
        await self.repo.delete(id_)

    async def list_(self, params: AuthorFilter = None) -> AuthorList:
        return await self.repo.list_(params)
