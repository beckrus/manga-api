from sqlalchemy import func, select
from src.schemas.authors import AuthorResponseDTO
from src.repositories.mappers.mappers import AuthorsMapper
from src.repositories.base import BaseRepository
from src.models.authors import AuthorsOrm


class AuthorsRepository(BaseRepository):
    model = AuthorsOrm
    mapper = AuthorsMapper

    async def get_filtered(self, name: str) -> list[AuthorResponseDTO]:
        query = (
            select(AuthorsOrm)
            .where(func.lower(self.model.name).contains(name.strip().lower()))
            .order_by(self.model.name)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self) -> list[AuthorResponseDTO]:
        query = select(self.model).order_by(self.model.name)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
