from pydantic import BaseModel


class ReaderRef(BaseModel):
    name: str
    email: str


class ReaderUpd(BaseModel):
    name: str | None = None
    email: str | None = None


class Reader(ReaderRef):
    id: int
