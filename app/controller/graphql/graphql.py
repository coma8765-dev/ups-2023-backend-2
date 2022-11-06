from datetime import timedelta

import asyncpg
import strawberry
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from strawberry.fastapi.router import BaseContext

from app.adapter.pg.session import storage
from app.controller.graphql.mutations import Mutation
from app.controller.graphql.queries import Query


class DBContext(BaseContext):
    db: asyncpg.Connection
    acquire: asyncpg.Pool.acquire

    def __init__(self):
        super().__init__()
        self.db: asyncpg.Connection = storage.pool
        self.acquire: asyncpg.Pool.acquire = storage.pool.acquire


def db_dependency() -> DBContext:
    return DBContext()


async def get_context(custom_context=Depends(db_dependency)):
    return custom_context


TimeDeltaScalar = strawberry.scalar(
    timedelta,
    serialize=lambda value: int(value.total_seconds()),
    parse_value=lambda value: timedelta(seconds=value),
)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    scalar_overrides={
        timedelta: TimeDeltaScalar,
    }
)
graphql_route = GraphQLRouter(
    schema,
    context_getter=get_context,
)
