import logging
from fastapi import UploadFile
from src.services.pages import PagesService
from src.services.purchases_chapters import PurchasesChaptersService
from src.schemas.chapters import ChapterAddDTO, ChapterDBAddDTO, ChapterPatchDTO
from src.exceptions import (
    ChapterDuplicateException,
    ChapterIsNotPurchasedException,
    ChapterNotFoundException,
    FKObjectNotFoundException,
    MangaNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.services.base import BaseService
from src.utils.check_file import file_inspection_and_save, rm_file, save_page_files


class ChaptersService(BaseService):
    async def get_chapters(self, manga_id: int):
        return await self.db.chapters.get_filtered(manga_id=manga_id)

    async def get_chapter_by_id(self, chapter_id: int, user_id: int | None = None):
        try:
            chapter = await self.db.chapters.get_one_by_id(chapter_id)
            if chapter.is_premium:
                if user_id:
                    is_purchased = await PurchasesChaptersService(self.db).is_purchased(
                        user_id, chapter_id
                    )
                    if not is_purchased:
                        raise ChapterIsNotPurchasedException
                else:
                    raise ChapterIsNotPurchasedException
            return chapter
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e

    async def get_next_chapter(self, chapter_id: int, manga_id: int, user_id: int | None = None):
        chapter = await self.db.chapters.get_next_chapter(chapter_id=chapter_id, manga_id=manga_id)
        if chapter.is_premium:
            if user_id:
                is_purchased = await PurchasesChaptersService(self.db).is_purchased(
                    user_id, chapter.id
                )
                if not is_purchased:
                    raise ChapterIsNotPurchasedException
            else:
                raise ChapterIsNotPurchasedException
        return chapter

    async def add_chapter(self, manga_id: int, user_id: int, data: ChapterAddDTO, file: UploadFile):
        file_path = None
        try:
            file_path = file_inspection_and_save(file)

            chapter_dto = ChapterDBAddDTO.model_validate(
                {**data.model_dump(), "manga_id": manga_id, "created_by": user_id}
            )
            chapter = await self.db.chapters.add(chapter_dto)
            logging.info(f"Chapter added: {chapter}")
            chapter_id = chapter.id
            pages_path = save_page_files(manga_id, chapter_id, file_path)
            logging.info(f"Pages saved: {pages_path}")
            for k, v in enumerate(pages_path):
                logging.info(f"Adding page {k + 1} with URL: {v}")
                await PagesService(self.db).add_page(
                    chapter_id=chapter_id, user_id=user_id, number=k + 1, url=v
                )
                logging.info(f"Page added: {k + 1, v}")
            await self.db.commit()
            logging.info(f"Chapter committed: {chapter}")
            return chapter
        except FKObjectNotFoundException as e:
            raise MangaNotFoundException from e
        except ObjectDuplicateException as e:
            raise ChapterDuplicateException from e
        finally:
            if file_path:
                rm_file(file_path)

    async def modify_chapter(
        self, user_id: int, chapter_id: int, data: ChapterPatchDTO, file: UploadFile | None = None
    ):
        file_path = None
        data = ChapterPatchDTO.model_validate(data.model_dump(exclude_none=True))
        try:
            chapter = await self.db.chapters.edit(id=chapter_id, data=data, exclude_unset=True)
            if file:
                file_path = file_inspection_and_save(file)
                pages_path = save_page_files(chapter.manga_id, chapter_id, file_path)
                for k, v in enumerate(pages_path):
                    await PagesService(self.db).put_page(
                        chapter_id=chapter_id, user_id=user_id, number=k + 1, url=v
                    )
            await self.db.commit()
            return chapter
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e
        finally:
            if file_path:
                rm_file(file_path)

    async def delete_chapter(self, chapters_id: int):
        try:
            await self.db.chapters.delete(id=chapters_id)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e
