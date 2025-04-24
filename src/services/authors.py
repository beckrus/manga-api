from src.exceptions import AuthorNotFoundException, ObjectNotFoundException
from src.schemas.authors import AuthorAddDTO, AuthorPatchDTO
from src.services.base import BaseService


class AuthorsService(BaseService):
    async def get_authors(self, name: str | None):
        if name:
            return await self.db.authors.get_filtered(name=name)
        return await self.db.authors.get_all()

    async def get_author(self, id: int):
        try:
            return await self.db.authors.get_one_by_id(id)
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def add_author(self, data: AuthorAddDTO | list[AuthorAddDTO]):
        if isinstance(data, list):
            result = await self.db.authors.add_bulk(data)
        else:
            result = await self.db.authors.add(data)
        await self.db.commit()
        return result

    async def modify_author(self, author_id: int, data: AuthorPatchDTO):
        try:
            result = await self.db.authors.edit(id=author_id, data=data, exclude_unset=True)
            await self.db.commit()
            return result
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def delete_author(self, author_id: int):
        try:
            await self.db.authors.delete(id=author_id)
            await self.db.commit()
        except ObjectNotFoundException:
            raise AuthorNotFoundException
