from src.services.purchases_chapters import PurchasesChaptersService
from src.schemas.pages import PageDBAddDTO, PagePatchDTO
from src.exceptions import (
    ChapterIsNotPurchasedException,
    ChapterNotFoundException,
    PageDuplicateException,
    PageNotFoundException,
    FKObjectNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.services.base import BaseService
from src.utils.check_file import rm_file


class PagesService(BaseService):
    async def get_pages(self, chapter_id: int, user_id: int | None = None):
        try:
            chapter = await self.db.chapters.get_one_by_id(chapter_id)
        except ObjectNotFoundException as e:
            raise ChapterNotFoundException from e
        if chapter.is_premium:
            if user_id:
                is_purchased = await PurchasesChaptersService(self.db).is_purchased(
                    user_id, chapter_id
                )
                if not is_purchased:
                    raise ChapterIsNotPurchasedException
            else:
                raise ChapterIsNotPurchasedException
        return await self.db.pages.get_filtered(chapter_id=chapter_id)

    async def get_page_by_id(self, chapter_id: int, number: int):
        try:
            page = await self.db.pages.get_one_or_none(chapter_id=chapter_id, number=number)
            if page is None:
                raise PageNotFoundException
            return page
        except ObjectNotFoundException as e:
            raise PageNotFoundException from e

    async def add_page(self, chapter_id: int, user_id: int, number: int, url: str):
        try:
            page = PageDBAddDTO.model_validate(
                {"number": number, "url": url, "chapter_id": chapter_id, "created_by": user_id}
            )
            result = await self.db.pages.add(page)
            await self.db.commit()
            return result
        except FKObjectNotFoundException as e:
            raise ChapterNotFoundException from e
        except ObjectDuplicateException as e:
            raise PageDuplicateException from e

    async def modify_page(self, page_id: int, data: PagePatchDTO):
        try:
            page = await self.db.pages.get_one_or_none(id=page_id)
            if page:
                result = await self.db.pages.edit(page.id, data=data, exclude_unset=True)
                await self.db.commit()
                return result
            else:
                raise PageNotFoundException
        except ObjectNotFoundException as e:
            raise PageNotFoundException from e
        except FKObjectNotFoundException as e:
            raise ChapterNotFoundException from e

    async def put_page(self, chapter_id: int, user_id: int, number: int, url: str):
        try:
            page = PageDBAddDTO.model_validate(
                {"number": number, "url": url, "chapter_id": chapter_id, "created_by": user_id}
            )
            if page:
                result = await self.db.pages.replace(page)
                await self.db.commit()
                return result
            else:
                raise PageNotFoundException
        except ObjectNotFoundException as e:
            raise PageNotFoundException from e
        except FKObjectNotFoundException as e:
            raise ChapterNotFoundException from e

    async def delete_page(self, page_id: int):
        try:
            page = await self.db.pages.get_one_by_id(id=page_id)
            rm_file(page.url)
            await self.db.pages.delete(id=page_id)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise PageNotFoundException from e
