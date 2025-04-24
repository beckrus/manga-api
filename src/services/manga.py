from src.schemas.manga import MangaAddDTO, MangaDBAddDTO, MangaPatchDTO
from src.api.dependencies import MangaFilterDep, PaginationDep
from src.exceptions import (
    AuthorNotFoundException,
    FKObjectNotFoundException,
    MangaNotFoundException,
    ObjectNotFoundException,
)
from src.services.base import BaseService


class MangaService(BaseService):
    async def get_manga(self, filter: MangaFilterDep, pagination: PaginationDep):
        return await self.db.manga.get_filtered(
            name=filter.name,
            author=filter.author,
            limit=pagination.per_page,
            offset=(pagination.page - 1) * pagination.per_page,
        )

    async def get_manga_by_id(self, id: int):
        try:
            return await self.db.manga.get_one_by_id(id)
        except ObjectNotFoundException as e:
            raise MangaNotFoundException from e

    async def add_manga(self, user_id: int, data: MangaAddDTO | list[MangaAddDTO]):
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
