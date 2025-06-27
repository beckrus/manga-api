from fastapi import UploadFile
from src.schemas.manga import MangaDBAddDTO, MangaPatchDTO
from src.api.dependencies import MangaFilterDep, PaginationDep
from src.exceptions import (
    AuthorNotFoundException,
    FKObjectNotFoundException,
    MangaDuplicateException,
    MangaNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.services.base import BaseService
from src.utils.check_file import save_manga_poster


class MangaService(BaseService):
    async def add_manga_poster(self, manga_id: int, file: UploadFile):
        try:
            manga = await self.get_manga_by_id(manga_id)
            file_path = save_manga_poster(manga_id, file)
            data = MangaPatchDTO.model_validate({"image": file_path})
            return await self.modify_manga(manga.id, data)
        except ObjectNotFoundException as e:
            raise MangaNotFoundException from e

    async def get_manga(self, filter: MangaFilterDep, pagination: PaginationDep):
        return await self.db.manga.get_filtered(
            name=filter.name,
            author=filter.author,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
            sort=pagination.sort,
        )

    async def get_manga_by_id(self, manga_id: int, user_id: int | None = None):
        try:
            return await self.db.manga.get_one_by_id_with_progress(manga_id, user_id)
        except ObjectNotFoundException as e:
            raise MangaNotFoundException from e

    async def add_manga(self, user_id: int, data: list[dict]):
        try:
            if isinstance(data, list):
                manga = [
                    MangaDBAddDTO.model_validate({**n.model_dump(), "created_by": user_id})
                    for n in data
                ]
                result = await self.db.manga.add_bulk(manga)
            else:
                manga = MangaDBAddDTO.model_validate({**data.model_dump(), "created_by": user_id})
                result = await self.db.manga.add(manga)
            await self.db.commit()
            return result
        except FKObjectNotFoundException as e:
            raise AuthorNotFoundException from e
        except ObjectDuplicateException as e:
            raise MangaDuplicateException from e

    async def modify_manga(self, manga_id: int, data: MangaPatchDTO):
        try:
            result = await self.db.manga.edit(id=manga_id, data=data, exclude_unset=True)
            await self.db.commit()
            return result
        except ObjectNotFoundException as e:
            raise MangaNotFoundException from e

    async def delete_manga(self, manga_id: int):
        try:
            await self.db.manga.delete(id=manga_id)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise MangaNotFoundException from e
