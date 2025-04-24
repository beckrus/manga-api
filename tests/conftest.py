# ruff: noqa: E402
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import json
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from src.api.dependencies import get_db, get_db_manager_null_pull
from src.schemas.authors import AuthorAddDTO
from src.schemas.manga import MangaDBAddDTO
from src.schemas.users import UserDBAddDTO
from src.database import engine_null_pool, Base
from src.models import *  # noqa: F403
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager


TEST_USERNAME = "admin"
TEST_PASSWORD = "12345678"


@pytest.fixture(autouse=True, scope="session")
async def check_mode() -> None:
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DBManager, Any]:
    async with get_db_manager_null_pull() as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture()
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def add_user(setup_database):
    async with get_db_manager_null_pull() as db:
        user_data = UserDBAddDTO.model_validate(
            {
                "username": TEST_USERNAME,
                "email": TEST_USERNAME + "@axeample.com",
                "password_hash": TEST_PASSWORD,
            }
        )
        result = await db.users.add(user_data)
        await db.commit()
        assert result.username == TEST_USERNAME


@pytest.fixture(autouse=True, scope="session")
async def add_authors(add_user):
    async with get_db_manager_null_pull() as db:
        with open("tests/mock_authors.json", "r") as f:
            data = json.loads(f.read())
            authors_data = [AuthorAddDTO.model_validate(n) for n in data]
        await db.authors.add_bulk(authors_data)
        await db.commit()
        authors_in_db = await db.authors.get_filtered()
        assert len(authors_data) == len(authors_in_db)


@pytest.fixture(autouse=True, scope="session")
async def add_manga(add_user):
    async with get_db_manager_null_pull() as db:
        with open("tests/mock_manga.json", "r") as f:
            data = json.loads(f.read())
            manga_data = [MangaDBAddDTO.model_validate(n) for n in data]
        await db.manga.add_bulk(manga_data)
        await db.commit()
        manga_in_db = await db.manga.get_all()
        assert len(manga_data) == len(manga_in_db)
