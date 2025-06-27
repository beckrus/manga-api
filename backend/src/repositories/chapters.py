from sqlalchemy import select
from src.schemas.chapters import ChapterResponseDTO, ChapterResponseWithPagesDTO
from src.exceptions import ChapterNotFoundException
from src.models.chapters import ChaptersOrm
from src.repositories.mappers.mappers import ChaptersMapper
from src.repositories.base import BaseRepository


class ChaptersRepository(BaseRepository):
    model = ChaptersOrm
    mapper = ChaptersMapper

    async def get_filtered(self, *filter, **filter_by) -> ChapterResponseDTO:
        query = (
            select(self.model).filter(*filter).filter_by(**filter_by).order_by(ChaptersOrm.number)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_next_chapter(self, chapter_id: int, manga_id: int) -> ChapterResponseWithPagesDTO:
        chapter = await self.get_one_or_none(manga_id=manga_id, id=chapter_id)
        if not chapter:
            raise ChapterNotFoundException
        next_chapter = await self.get_one_or_none(manga_id=manga_id, number=chapter.number + 1)
        if next_chapter:
            return next_chapter
        raise ChapterNotFoundException
