from abc import ABC, abstractmethod

from fastapi import Depends

from app.domain.entity.rentals import *
from app.domain.exc import BadRequest
from app.domain.service.books import BooksStorage


class RentalsStorage(ABC):
    @abstractmethod
    async def create(self, ref: RentalRef) -> Rental:
        ...

    @abstractmethod
    async def update(self, id_: int, ref: RentalUpd):
        ...

    @abstractmethod
    async def get_by_book_and_reader(self, reader_id: int,
                                     book_id: int) -> Rental:
        ...

    @abstractmethod
    async def list_(self, params: RentalFilter) -> RentalList:
        ...


class RentalsService:
    __slots__ = ("repo", "book_repo")
    repo: RentalsStorage
    book_repo: BooksStorage | None

    def __init__(
            self,
            repo: RentalsStorage = Depends(),
            book_repo: BooksStorage | None = None,
    ):
        self.repo = repo
        self.book_repo = book_repo

    async def rent(self, ref: RentalRef) -> Rental:
        if (await self.book_repo.get(ref.book_id)).is_busy:
            raise BadRequest("Already booked")
        return await self.repo.create(ref)

    async def return_(self, ref: RentalRef):
        rental = await self.repo.get_by_book_and_reader(
            ref.reader_id,
            ref.book_id,
        )

        await self.repo.update(rental.id, RentalUpd(end=datetime.now()))
        return await self.repo.get_by_book_and_reader(
            ref.reader_id,
            ref.book_id,
        )

    async def list_(
            self,
            params: RentalFilter = RentalFilter()
    ) -> list[Rental]:
        return await self.repo.list_(params)
