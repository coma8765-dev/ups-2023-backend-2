import strawberry
from strawberry.types import Info

from app.controller.graphql.types import AuthorType, BookType, ReaderType, \
    RentalType
from app.domain.entity.rentals import RentalFilter
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.repo.books import BooksPGStorage
from app.domain.repo.readers import ReadersPGStorage
from app.domain.repo.rentals import RentalsPGStorage
from app.domain.service.authors import AuthorsService
from app.domain.service.books import BooksService
from app.domain.service.readers import ReadersService
from app.domain.service.rentals import RentalsService


@strawberry.type
class Query:
    @strawberry.field()
    async def authors(self, info: Info) -> list[AuthorType]:
        use_case = AuthorsService(AuthorsPGStorage(info.context.db))
        return [AuthorType.from_pydantic(i) for i in await use_case.list_()]

    @strawberry.field()
    async def books(self, info: Info) -> list[BookType]:
        use_case = BooksService(BooksPGStorage(info.context.db))
        return [BookType.from_pydantic(i) for i in await use_case.list_()]

    @strawberry.field()
    async def author(self, ID: int, info: Info) -> AuthorType:
        use_case = AuthorsService(AuthorsPGStorage(info.context.db))
        return AuthorType.from_pydantic(await use_case.get(ID))

    @strawberry.field()
    async def book(self, ID: int, info: Info) -> BookType:
        use_case = BooksService(BooksPGStorage(info.context.db))
        return BookType.from_pydantic(await use_case.get(ID))

    @strawberry.field()
    async def reader(self, ID: int, info: Info) -> ReaderType:
        use_case = ReadersService(ReadersPGStorage(info.context.db))
        return ReaderType.from_pydantic(await use_case.get(ID))

    @strawberry.field()
    async def rents(self, reader_id: int, info: Info) -> list[RentalType]:
        use_case = RentalsService(RentalsPGStorage(info.context.db))
        return [
            RentalType.from_pydantic(i)
            for i in await use_case.list_(RentalFilter(reader_id=reader_id))]
