from datetime import datetime

from pydantic import BaseModel, Field


class AuthorRef(BaseModel):
    name: str
    image_link: str
    birthdate: datetime
    death_date: datetime | None


class AuthorUpd(BaseModel):
    name: str | None = None
    image_link: str | None = None
    birthdate: datetime | None = None
    death_date: datetime | None = None


class Author(AuthorRef):
    id: int


class AuthorFilter(BaseModel):
    # TODO(additional): Implement filter, such as page, limit and others
    ...


class AuthorList(BaseModel):
    __root__ = list[Author]
