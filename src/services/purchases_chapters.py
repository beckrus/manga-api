from src.schemas.users import UserPatchCoinsDTO
from src.schemas.purchases_chapters import PurchasesChaptersDBAddDTO
from src.exceptions import (
    ChapterIsFreeException,
    ChapterNotFoundException,
    FKObjectNotFoundException,
    NotEnoughtCoinsException,
    ObjectDuplicateException,
    PurchasesChapterDuplicateException,
)
from src.services.base import BaseService


class PurchasesChaptersService(BaseService):
    async def all_purchases(self):
        return await self.db.purchases_chapters.get_all()

    async def my_purchases(self, user_id: int) -> None:
        return await self.db.purchases_chapters.get_filtered(user_id=user_id)

    async def purchase_chapter(self, user_id: int, chapter_id: int) -> None:
        try:
            user = await self.db.users.get_one_by_id(user_id)
            chapter = await self.db.chapters.get_one_by_id(chapter_id)
            if not chapter.is_premium:
                raise ChapterIsFreeException
            price = chapter.price
            new_coin_balance = user.coin_balance - price
            if new_coin_balance < 0:
                raise NotEnoughtCoinsException
            data = PurchasesChaptersDBAddDTO.model_validate(
                {"user_id": user_id, "chapter_id": chapter_id, "price": price}
            )
            await self.db.purchases_chapters.add(data)
            user_data = UserPatchCoinsDTO.model_validate({"coin_balance": new_coin_balance})
            await self.db.users.edit(user_id, user_data, exclude_unset=True)
            await self.db.commit()
        except ObjectDuplicateException as e:
            raise PurchasesChapterDuplicateException from e
        except FKObjectNotFoundException as e:
            raise ChapterNotFoundException from e
