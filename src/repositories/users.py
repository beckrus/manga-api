from src.models.users import UserOrm
from src.repositories.mappers.mappers import UserMapper
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserOrm
    mapper = UserMapper
