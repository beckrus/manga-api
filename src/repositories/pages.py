from sqlalchemy import select
from src.schemas.pages import PageResponseDTO
from src.models.pages import PagesOrm
from src.repositories.mappers.mappers import PagesMapper
from src.repositories.base import BaseRepository


class PagesRepository(BaseRepository):
    model = PagesOrm
    mapper = PagesMapper

    async def get_filtered(self, *filter, **filter_by) -> list[PageResponseDTO]:
        query = select(self.model).filter(*filter).filter_by(**filter_by).order_by(PagesOrm.number)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
