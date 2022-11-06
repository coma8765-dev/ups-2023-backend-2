from typing import Annotated

import strawberry
from strawberry.types import Info

from app.domain.entity.authors import Author
from app.domain.entity.books import Book, BookFilter
from app.domain.entity.readers import Reader
from app.domain.entity.rentals import Rental, RentalFilter
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.repo.books import BooksPGStorage
from app.domain.repo.readers import ReadersPGStorage
from app.domain.repo.rentals import RentalsPGStorage
from app.domain.service.authors import AuthorsService
from app.domain.service.books import BooksService
from app.domain.service.readers import ReadersService
from app.domain.service.rentals import RentalsService


@strawberry.experimental.pydantic.type(model=Rental, all_fields=True)
class RentalType:
    @strawberry.field()
    async def book(
            self,
            info: Info,
    ) -> Annotated["BookType", strawberry.lazy(".types")]:
        use_case = BooksService(BooksPGStorage(info.context.db))
        return BookType.from_pydantic(await use_case.get(self.book_id))

    @strawberry.field()
    async def reader(
            self,
            info: Info,
    ) -> Annotated["ReaderType", strawberry.lazy(".types")]:
        use_case = ReadersService(ReadersPGStorage(info.context.db))
        return ReaderType.from_pydantic(await use_case.get(self.reader_id))


@strawberry.experimental.pydantic.type(model=Reader, all_fields=True)
class ReaderType:
    @strawberry.field()
    async def rents(self, info: Info) -> list[RentalType]:
        use_case = RentalsService(RentalsPGStorage(info.context.db))
        return [RentalType.from_pydantic(i)
                for i in await use_case.list_(RentalFilter(reader_id=self.id))]

    @strawberry.field()
    async def fine_amount(self, info: Info) -> int:
        use_case = RentalsService(RentalsPGStorage(info.context.db))
        return sum(
            i.fine_amount * (i.rental_time.days - i.rental_limit.days)
            for i in await use_case.list_(RentalFilter(
                reader_id=self.id,
                is_returned=True,
            ))
            if i.rental_time and i.rental_time > i.rental_limit
        )


@strawberry.experimental.pydantic.type(model=Book, all_fields=True)
class BookType:
    @strawberry.field()
    async def author(
            self,
            info: Info,
    ) -> Annotated["AuthorType", strawberry.lazy(".types")]:
        use_case = AuthorsService(AuthorsPGStorage(info.context.db))
        return AuthorType.from_pydantic(await use_case.get(self.author_id))

    @strawberry.field()
    async def rentals(
            self,
            info: Info,
    ) -> list[Annotated["RentalType", strawberry.lazy(".types")]]:
        use_case = RentalsService(RentalsPGStorage(info.context.db))
        return list(map(
            RentalType.from_pydantic,
            await use_case.list_(RentalFilter(book_id=self.id)),
        ))


@strawberry.experimental.pydantic.type(model=Author, all_fields=True)
class AuthorType:
    @strawberry.field()
    async def books(self, info: Info) -> list["BookType"]:
        use_case = BooksService(BooksPGStorage(info.context.db))
        return [BookType.from_pydantic(i)
                for i in await use_case.list_(BookFilter(author_id=self.id))]

    @strawberry.field()
    async def available_books(self, info: Info) -> list["BookType"]:
        use_case = BooksService(BooksPGStorage(info.context.db))
        return [BookType.from_pydantic(i)
                for i in await use_case.list_(BookFilter(author_id=self.id,
                                                         is_available=True))]
