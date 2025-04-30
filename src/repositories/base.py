import logging
from typing import Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.repositories.mappers.base import BaseMapper
from src.exceptions import (
    FKObjectNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.database import Base
from utils.re import get_missing_fk

# Type definition for Model
DBModelType = TypeVar("DBModelType", bound=Base)
# Type definition for Schema
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(Generic[DBModelType, SchemaType]):
    model: type[DBModelType]
    mapper: BaseMapper

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[SchemaType]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self) -> list[SchemaType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filters_by) -> SchemaType | None:
        query = select(self.model).filter_by(**filters_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one_by_id(self, id: int) -> SchemaType:
        try:
            query = select(self.model).filter_by(id=id)
            result = await self.session.execute(query)
            data = result.scalars().one()
            return self.mapper.map_to_domain_entity(data)
        except NoResultFound as e:
            raise ObjectNotFoundException from e

    async def add(self, data: SchemaType) -> None:
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
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

    async def add_bulk(self, data: list[SchemaType]) -> list[SchemaType]:
        try:
            stmt = (
                insert(self.model)
                .values([item.model_dump() for item in data])
                .on_conflict_do_nothing()
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            return [self.mapper.map_to_domain_entity(n) for n in result.scalars().all()]
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
                    f"Unknown error occurred, error type: {type(e.orig.__cause__)=}, input {data=}, source: BaseRepository.add_bulk"
                )
                raise e

    async def edit(self, id: int, data: SchemaType, exclude_unset: bool = False) -> SchemaType:
        try:
            stmt = (
                update(self.model)
                .filter_by(id=id)
                .values(**data.model_dump(exclude_unset=exclude_unset))
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except NoResultFound as e:
            raise ObjectNotFoundException from e

    async def delete(self, id) -> None:
        stmt = delete(self.model).filter_by(id=id)
        result = await self.session.execute(stmt)
        if result.rowcount < 1:
            raise ObjectNotFoundException

    async def delete_bulk(self, ids: list[int]) -> None:
        stmt = delete(self.model).filter(self.model.id.in_(ids))
        result = await self.session.execute(stmt)

        if result.rowcount < len(ids):
            raise ObjectNotFoundException
