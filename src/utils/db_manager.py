from collections.abc import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.pages import PagesRepository
from src.repositories.chapters import ChaptersRepository
from src.repositories.users import UsersRepository
from src.repositories.manga import MangaRepository
from src.repositories.authors import AuthorsRepository


class DBManager:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.authors = AuthorsRepository(self.session)
        self.manga = MangaRepository(self.session)
        self.users = UsersRepository(self.session)
        self.chapters = ChaptersRepository(self.session)
        self.pages = PagesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    def __repr__(self):
        return "DBManager"
