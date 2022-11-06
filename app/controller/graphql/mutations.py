from datetime import datetime, timedelta

import strawberry
from strawberry.types import Info

from app.adapter.pg.session import storage
from app.controller.graphql.types import AuthorType, BookType, ReaderType, \
    RentalType
from app.domain.entity.authors import AuthorRef, AuthorUpd
from app.domain.entity.books import BookRef, BookUpd
from app.domain.entity.readers import ReaderRef, ReaderUpd
from app.domain.entity.rentals import RentalRef
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.repo.books import BooksPGStorage
from app.domain.repo.readers import ReadersPGStorage
from app.domain.repo.rentals import RentalsPGStorage
from app.domain.service.authors import AuthorsService
from app.domain.service.books import BooksService
from app.domain.service.readers import ReadersService
from app.domain.service.rentals import RentalsService


@strawberry.type
class Mutation:
    @strawberry.mutation()
    async def add_author(
            self,
            info: Info,
            name: str,
            image_link: str,
            birthdate: datetime,
            death_date: datetime | None = None,
    ) -> AuthorType:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = AuthorsService(AuthorsPGStorage(conn))
                return AuthorType.from_pydantic(
                    await use_case.create(AuthorRef(
                        name=name,
                        image_link=image_link,
                        birthdate=birthdate,
                        death_date=death_date,
                    )))

    @strawberry.mutation()
    async def update_author(
            self,
            info: Info,
            ID: int,
            name: str | None = None,
            image_link: str | None = None,
            birthdate: datetime | None = None,
            death_date: datetime | None = None,
    ) -> None:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = AuthorsService(AuthorsPGStorage(conn))
                await use_case.update(
                    ID,
                    AuthorUpd(
                        name=name,
                        image_link=image_link,
                        birthdate=birthdate,
                        death_date=death_date,
                    ))

    @strawberry.mutation()
    async def delete_author(
            self,
            info: Info,
            ID: int,
    ) -> None:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = AuthorsService(AuthorsPGStorage(conn))
                await use_case.delete(ID)

    @strawberry.mutation()
    async def add_book(
            self,
            info: Info,
            title: str,
            rental_limit: timedelta | None,
            image_link: str | None,
            author_id: int,
    ) -> BookType:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = BooksService(BooksPGStorage(conn))
                return BookType.from_pydantic(
                    await use_case.create(BookRef(
                        title=title,
                        rental_limit=rental_limit,
                        image_link=image_link,
                        author_id=author_id,
                    )))

    @strawberry.mutation()
    async def update_book(
            self,
            info: Info,
            ID: int,
            title: str | None = None,
            rental_limit: timedelta | None = None,
            image_link: str | None = None,
            author_id: int | None = None,
    ) -> None:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = BooksService(BooksPGStorage(conn))
                await use_case.update(
                    ID,
                    BookUpd(
                        title=title,
                        rental_limit=rental_limit,
                        image_link=image_link,
                        author_id=author_id,
                    ))

    @strawberry.mutation()
    async def delete_book(
            self,
            info: Info,
            ID: int,
    ) -> None:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = BooksService(BooksPGStorage(conn))
                await use_case.delete(ID)

    @strawberry.mutation()
    async def add_reader(
            self,
            info: Info,
            name: str,
            email: str,
    ) -> ReaderType:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = ReadersService(ReadersPGStorage(conn))
                return ReaderType.from_pydantic(await use_case.create(
                    ReaderRef(
                        name=name,
                        email=email,
                    )))

    @strawberry.mutation()
    async def update_reader(
            self,
            info: Info,
            ID: int,
            name: str | None = None,
            email: str | None = None,
    ) -> None:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = ReadersService(ReadersPGStorage(conn))
                await use_case.update(
                    ID,
                    ReaderUpd(
                        name=name,
                        email=email,
                    ))

    @strawberry.mutation()
    async def delete_reader(
            self,
            info: Info,
            ID: int,
    ) -> None:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = ReadersService(ReadersPGStorage(conn))
                await use_case.delete(ID)

    @strawberry.mutation()
    async def rent_book(
            self,
            info: Info,
            book_id: int,
            reader_id: int,
    ) -> RentalType:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = RentalsService(RentalsPGStorage(conn),
                                          BooksPGStorage(conn))
                return RentalType.from_pydantic(await use_case.rent(RentalRef(
                    book_id=book_id,
                    reader_id=reader_id,
                )))

    @strawberry.mutation()
    async def return_book(
            self,
            info: Info,
            book_id: int,
            reader_id: int,
    ) -> RentalType:
        async with info.context.acquire() as conn:
            async with conn.transaction():
                use_case = RentalsService(RentalsPGStorage(conn))
                return RentalType.from_pydantic(await use_case.return_(
                    RentalRef(
                        book_id=book_id,
                        reader_id=reader_id,
                    )))
