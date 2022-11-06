import random
from datetime import datetime, timedelta

from pydantic import BaseModel, Field, validator


class RentalRef(BaseModel):
    book_id: int
    reader_id: int
    fine_amount: int = Field(default_factory=lambda: random.randint(0, 1000))


class Rental(RentalRef):
    id: int
    start: datetime
    end: datetime | None
    rental_time: timedelta | None = None
    rental_limit: timedelta | None = None

    # noinspection PyMethodParameters,PyUnusedLocal
    @validator("rental_time", always=True)
    def calculate_time(cls, v, values, **kwargs):
        if values["end"]:
            return values["end"] - values["start"]


class RentalUpd(BaseModel):
    end: datetime | None = None


class RentalFilter(BaseModel):
    book_id: int | None = None
    reader_id: int | None = None
    is_returned: bool | None = None


class RentalList(BaseModel):
    __root__ = list[Rental]
