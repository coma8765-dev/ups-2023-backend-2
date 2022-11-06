from fastapi import FastAPI

from app.adapter.pg.session import storage
from app.controller.graphql.graphql import graphql_route
from app.domain.provider.storage.storage import StorageProvider
from app.domain.repo.authors import AuthorsPGStorage
from app.domain.repo.books import BooksPGStorage
from app.domain.repo.readers import ReadersPGStorage
from app.domain.repo.rentals import RentalsPGStorage
from app.domain.service.authors import AuthorsStorage
from app.domain.service.books import BooksStorage
from app.domain.service.readers import ReadersStorage
from app.domain.service.rentals import RentalsStorage

app = FastAPI()

app.on_event("startup")(storage.startup)
app.dependency_overrides[StorageProvider] = storage
app.dependency_overrides[AuthorsStorage] = AuthorsPGStorage
app.dependency_overrides[BooksStorage] = BooksPGStorage
app.dependency_overrides[ReadersStorage] = ReadersPGStorage
app.dependency_overrides[RentalsStorage] = RentalsPGStorage

app.include_router(graphql_route, prefix="/graphql")
