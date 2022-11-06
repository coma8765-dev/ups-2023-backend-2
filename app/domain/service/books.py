from abc import ABC, abstractmethod

from fastapi import Depends

from app.domain.entity.books import *


class BooksStorage(ABC):
    @abstractmethod
    async def create(self, ref: BookRef) -> Book:
        ...

    @abstractmethod
    async def update(self, id_: int, ref: BookUpd):
        ...

    @abstractmethod
    async def delete(self, id_: int):
        ...

    @abstractmethod
    async def get(self, id_: int) -> Book:
        ...

    @abstractmethod
    async def list_(self, params: BookFilter) -> BookList:
        ...


class BooksService:
    __slots__ = ("repo",)
    repo: BooksStorage

    def __init__(self, repo: BooksStorage = Depends()):
        self.repo = repo

    async def create(self, ref: BookRef) -> Book:
        return await self.repo.create(ref)

    async def update(self, id_: int, upd: BookUpd):
        await self.repo.update(id_, upd)

    async def get(self, id_: int) -> Book:
        return await self.repo.get(id_)

    async def delete(self, id_: int):
        await self.repo.delete(id_)

    async def list_(self, params: BookFilter = BookFilter()) -> list[Book]:
        return await self.repo.list_(params)

