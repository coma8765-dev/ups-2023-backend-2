from datetime import timedelta

from pydantic import BaseModel, validator


class BookRef(BaseModel):
    title: str
    rental_limit: timedelta | None
    image_link: str | None
    author_id: int

    rental_limit_seconds: int | None = None
    is_busy: bool = True

    # noinspection PyMethodParameters
    @validator("rental_limit_seconds", always=True)
    def _set_rental_limit_seconds(cls, v, values, **kwargs):
        if values["rental_limit"]:
            return values["rental_limit"].total_seconds()


class Book(BookRef):
    id: int


class BookUpd(BaseModel):
    title: str | None = None
    rental_limit: timedelta | None = None
    image_link: str | None = None
    author_id: int | None = None


class BookFilter(BaseModel):
    title: str | None = None
    author_id: int | None = None
    is_available: bool | None = None


class BookList(BaseModel):
    __root__ = list[Book]
