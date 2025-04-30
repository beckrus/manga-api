from src.exceptions import ChapterNotFoundException
from src.models.favorites import FavoriteMangaOrm
from src.repositories.mappers.mappers import FavoriteMangaMapper
from src.repositories.base import BaseRepository


class FavoritesRepository(BaseRepository):
    model = FavoriteMangaOrm
    mapper = FavoriteMangaMapper

    async def get_page_by_manga_and_number(self, chapter_number, manga_id):
        chapter = await self.get_one_or_none(manga_id=manga_id, number=chapter_number)
        if chapter:
            return chapter
        raise ChapterNotFoundException
