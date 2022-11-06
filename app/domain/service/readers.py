from abc import ABC, abstractmethod

from fastapi import Depends

from app.domain.entity.readers import *


class ReadersStorage(ABC):
    @abstractmethod
    async def create(self, ref: ReaderRef) -> Reader:
        ...

    @abstractmethod
    async def update(self, id_: int, ref: ReaderUpd):
        ...

    @abstractmethod
    async def delete(self, id_: int):
        ...

    @abstractmethod
    async def get(self, id_: int) -> Reader:
        ...


class ReadersService:
    __slots__ = ("repo",)
    repo: ReadersStorage

    def __init__(self, repo: ReadersStorage = Depends()):
        self.repo = repo

    async def create(self, ref: ReaderRef) -> Reader:
        return await self.repo.create(ref)

    async def update(self, id_: int, upd: ReaderUpd):
        await self.repo.update(id_, upd)

    async def get(self, id_: int) -> Reader:
        return await self.repo.get(id_)

    async def delete(self, id_: int):
        await self.repo.delete(id_)
