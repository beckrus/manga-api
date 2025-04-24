from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends

from src.schemas.filters import MangaFilterSchema, PaginationParamsSchema
from src.utils.db_manager import DBManager
from src.database import async_session_maker, async_session_maker_null_pool

PaginationDep = Annotated[PaginationParamsSchema, Depends()]

MangaFilterDep = Annotated[MangaFilterSchema, Depends()]


def get_db_manager() -> DBManager:
    return DBManager(session_factory=async_session_maker)


def get_db_manager_null_pull() -> DBManager:
    return DBManager(session_factory=async_session_maker_null_pool)


async def get_db() -> AsyncGenerator[DBManager, Any]:
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
