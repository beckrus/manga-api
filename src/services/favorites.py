from src.schemas.favorites import FavoriteMangaDTO
from src.schemas.manga import MangaChangeBookmarksCountDTO, MangaResponseDTO
from src.exceptions import (
    FKObjectNotFoundException,
    FavoriteNotFoundException,
    MangaNotFoundException,
    ObjectNotFoundException,
    FavoriteDuplicateException,
    ObjectDuplicateException,
)
from src.services.base import BaseService


class FavoritesService(BaseService):
    async def get_favorites(self, user_id: int) -> list[MangaResponseDTO]:
        fav_list = await self.db.favorites.get_filtered(user_id=user_id)
        fav_ids = [n.manga_id for n in fav_list]
        fav_manga = await self.db.manga.get_filtered_by_ids(fav_ids)
        return fav_manga

    async def add_to_favorite(self, manga_id: int, user_id: int):
        try:
            data = FavoriteMangaDTO.model_validate({"manga_id": manga_id, "user_id": user_id})
            manga = await self.db.manga.get_one_by_id(manga_id)
            update_manga = MangaChangeBookmarksCountDTO.model_validate(
                {"count_bookmarks": manga.count_bookmarks + 1}
            )
            await self.db.favorites.add(data)
            await self.db.manga.edit(manga_id, update_manga, exclude_unset=True)
            await self.db.commit()
        except ObjectDuplicateException as e:
            raise FavoriteDuplicateException from e
        except FKObjectNotFoundException as e:
            raise MangaNotFoundException from e

    async def delete_favorite(self, manga_id: int, user_id: int) -> None:
        try:
            fav_id = await self.db.favorites.get_one_or_none(manga_id=manga_id, user_id=user_id)
            if not fav_id:
                raise FavoriteNotFoundException
            manga = await self.db.manga.get_one_by_id(manga_id)
            counts = 0 if manga.count_bookmarks - 1 < 0 else manga.count_bookmarks - 1
            update_manga = MangaChangeBookmarksCountDTO.model_validate({"count_bookmarks": counts})
            await self.db.favorites.delete(fav_id.id)
            await self.db.manga.edit(manga_id, update_manga, exclude_unset=True)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise FavoriteNotFoundException from e
