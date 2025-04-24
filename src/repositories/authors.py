from src.repositories.mappers.mappers import AuthorsMapper
from src.repositories.base import BaseRepository
from src.models.authors import AuthorsOrm


class AuthorsRepository(BaseRepository):
    model = AuthorsOrm
    mapper = AuthorsMapper
