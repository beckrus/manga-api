import logging
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from src.exceptions import FKObjectNotFoundException
from src.schemas.pages import PageDBAddDTO, PageResponseDTO
from src.models.pages import PagesOrm
from src.repositories.mappers.mappers import PagesMapper
from src.repositories.base import BaseRepository
from src.utils.re import get_missing_fk


class PagesRepository(BaseRepository):
    model = PagesOrm
    mapper = PagesMapper

    async def get_filtered(self, *filter, **filter_by) -> list[PageResponseDTO]:
        query = select(self.model).filter(*filter).filter_by(**filter_by).order_by(PagesOrm.number)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def replace(self, data: PageDBAddDTO) -> None:
        try:
            pk_constraint_name = "_uniq_chapter_page"
            stmt = (
                insert(self.model)
                .values(**data.model_dump())
                .on_conflict_do_update(
                    constraint=pk_constraint_name, set_=dict(**data.model_dump())
                )
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except IntegrityError as e:
            logging.error(
                f"Can't add data in DB, error type: {type(e.orig.__cause__)=}, input {data=}"
            )
            if e.orig.sqlstate == "23503":
                key, value = get_missing_fk(str(e))
                logging.error(f"Missing Key:{key}, Value:{value}")
                raise FKObjectNotFoundException from e
            else:
                logging.critical(
                    f"Unknown error occurred, error type: {type(e.orig.__cause__)=}, input {data=}, source: BaseRepository.add"
                )
                raise e
