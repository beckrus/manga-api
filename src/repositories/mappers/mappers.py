from src.schemas.authors import AuthorResponseFullDTO
from src.models.authors import AuthorsOrm
from src.repositories.mappers.base import BaseMapper


class AuthorsMapper(BaseMapper):
    model: AuthorsOrm
    schema: AuthorResponseFullDTO
