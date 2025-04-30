import logging
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from src.exceptions import FKObjectNotFoundException, ObjectDuplicateException
from src.schemas.read_progress import ReadProgressDTO
from src.models.read_progress import ReadProgressOrm
from src.repositories.mappers.mappers import ReadProgressMapper
from src.repositories.base import BaseRepository
from src.utils.re import get_missing_fk


class ReadingProgressRepository(BaseRepository):
    model = ReadProgressOrm
    mapper = ReadProgressMapper

    async def add(self, data: ReadProgressDTO) -> None:
        try:
            stmt = (
                insert(self.model)
                .values(**data.model_dump())
                .on_conflict_do_update(
                    constraint="_user_manga_read_progress", set_=dict(chapter_id=data.chapter_id)
                )
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except IntegrityError as e:
            logging.error(
                f"Can't add data in DB, error type: {type(e.orig.__cause__)=}, input {data=}"
            )
            if e.orig.sqlstate == "23505":
                raise ObjectDuplicateException from e
            elif e.orig.sqlstate == "23503":
                key, value = get_missing_fk(str(e))
                logging.error(f"Missing Key:{key}, Value:{value}")
                raise FKObjectNotFoundException from e
            else:
                logging.critical(
                    f"Unknown error occurred, error type: {type(e.orig.__cause__)=}, input {data=}, source: BaseRepository.add"
                )
                raise e
