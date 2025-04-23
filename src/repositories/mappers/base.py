from typing import Generic, TypeVar

from pydantic import BaseModel

from database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseMapper(Generic[DBModelType, SchemaType]):
    model: type[DBModelType]
    schema: type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data: DBModelType) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: SchemaType | dict) -> DBModelType:
        return cls.model(**data.model_dump() if not isinstance(data, dict) else data)
