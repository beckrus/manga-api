from src.schemas.chapters import ChapterAddDTO, ChapterDBAddDTO, ChapterPatchDTO
from src.exceptions import (
    ChapterDuplicateException,
    ChapterNotFoundException,
    FKObjectNotFoundException,
    MangaNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.services.base import BaseService


class ChaptersService(BaseService):
    async def get_chapters(self, manga_id: int):
        return await self.db.chapters.get_filtered(manga_id=manga_id)

    async def get_chapter_by_id(self, id: int):
        try:
            return await self.db.chapters.get_one_by_id(id)
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e

    async def get_next_chapter(self, chapter_id: int, manga_id: int):
        return await self.db.chapters.get_next_chapter(chapter_id=chapter_id, manga_id=manga_id)

    async def add_chapter(self, manga_id: int, user_id: int, data: ChapterAddDTO):
        try:
            chapters = ChapterDBAddDTO.model_validate(
                {**data.model_dump(), "manga_id": manga_id, "created_by": user_id}
            )
            result = await self.db.chapters.add(chapters)
            return result
        except FKObjectNotFoundException as e:
            raise MangaNotFoundException from e
        except ObjectDuplicateException as e:
            raise ChapterDuplicateException from e

    async def modify_chapter(self, chapter_id: int, data: ChapterPatchDTO):
        try:
            result = await self.db.chapters.edit(id=chapter_id, data=data, exclude_unset=True)
            await self.db.commit()
            return result
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e

    async def delete_chapter(self, chapters_id: int):
        try:
            await self.db.chapters.delete(id=chapters_id)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e
