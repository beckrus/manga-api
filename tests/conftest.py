# ruff: noqa: E402
from unittest import mock
from unittest.mock import AsyncMock, MagicMock
import pytest


# patch fastapi_chache
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

# patch redis_manager
mock_instance = MagicMock()
mock_instance.get = AsyncMock(return_value=None)
mock_instance.set = AsyncMock()
mock_instance.delete = AsyncMock()
mock_instance.close = AsyncMock()
mock.patch("src.utils.redis_connector.redis_manager", mock_instance).start()


import json
from typing import Any, AsyncGenerator, Final
from httpx import ASGITransport, AsyncClient
from src.api.dependencies import get_db, get_db_manager_null_pull
from src.schemas.authors import AuthorAddDTO
from src.schemas.manga import MangaDBAddDTO
from src.schemas.chapters import ChapterDBAddDTO
from src.database import engine_null_pool, Base
from src.models import *  # noqa: F403
from src.config import settings
from src.main import app
from src.utils.db_manager import DBManager


TEST_FIRST_USERNAME: Final = "admin"
TEST_FIRST_PASSWORD: Final = "12345678"

TEST_SECOND_USERNAME: Final = "user"
TEST_SECOND_PASSWORD: Final = "87654321"


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


@pytest.fixture()
async def ac_auth(add_user) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/auth/login", data={"username": TEST_FIRST_USERNAME, "password": TEST_FIRST_PASSWORD}
        )
        assert res.status_code == 200
        res_data = res.json()
        access_token = res_data.get("access_token")
        assert access_token
        refresh_token = ac.cookies.get("refresh_token")
        assert refresh_token

        async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
            headers={"Authorization": f"Bearer {access_token}"},
            cookies={"refresh_token": refresh_token},
        ) as ac_auth:
            yield ac_auth


@pytest.fixture()
async def ac_auth_user(add_user) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res = await ac.post(
            "/auth/login", data={"username": TEST_SECOND_USERNAME, "password": TEST_SECOND_PASSWORD}
        )
        assert res.status_code == 200
        assert ac.cookies.get("access_token")
        assert ac.cookies.get("refresh_token")
        yield ac


@pytest.fixture(autouse=True, scope="session")
async def setup_database(check_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="session")
async def add_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        res_register = await ac.post(
            "/auth/register",
            json={
                "username": TEST_FIRST_USERNAME,
                "email": f"{TEST_FIRST_USERNAME}@example.com",
                "password": TEST_FIRST_PASSWORD,
                "password_confirm": TEST_FIRST_PASSWORD,
            },
        )
        assert res_register.status_code == 200
        res_register_2 = await ac.post(
            "/auth/register",
            json={
                "username": TEST_SECOND_USERNAME,
                "email": f"{TEST_SECOND_USERNAME}@example.com",
                "password": TEST_SECOND_PASSWORD,
                "password_confirm": TEST_SECOND_PASSWORD,
            },
        )
        assert res_register_2.status_code == 200


@pytest.fixture(autouse=True, scope="session")
async def add_authors(add_user):
    async with get_db_manager_null_pull() as db:
        with open("tests/mock_authors.json", "r") as f:
            data = json.loads(f.read())
            authors_data = [AuthorAddDTO.model_validate(n) for n in data]
        await db.authors.add_bulk(authors_data)
        await db.commit()
        authors_in_db = await db.authors.get_all()
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


@pytest.fixture(autouse=True, scope="session")
async def add_chapters(add_user, add_manga):
    async with get_db_manager_null_pull() as db:
        with open("tests/mock_chapters.json", "r") as f:
            data = json.loads(f.read())
            chapters_data = [ChapterDBAddDTO.model_validate(n) for n in data]
        await db.chapters.add_bulk(chapters_data)
        await db.commit()
        chapters_in_db = await db.chapters.get_all()
        assert len(chapters_data) == len(chapters_in_db)
