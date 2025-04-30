from sqlalchemy import func, or_, select
from exceptions import ObjectNotFoundException
from src.schemas.users import UserHashedPwdDTO
from src.models.users import UserOrm
from src.repositories.mappers.mappers import UserMapper
from src.repositories.base import BaseRepository
from sqlalchemy.exc import NoResultFound


class UsersRepository(BaseRepository):
    model = UserOrm
    mapper = UserMapper

    async def count_users(self):
        query = select(func.count()).select_from(UserOrm)
        result = await self.session.execute(query)
        data = result.scalars().one()
        return data

    async def get_one_by_name_or_email(self, username: str) -> UserHashedPwdDTO:
        try:
            query = select(self.model).where(
                or_(self.model.username == username, self.model.email == username)
            )
            result = await self.session.execute(query)
            data = result.scalars().one()
            return UserHashedPwdDTO.model_validate(data, from_attributes=True)
        except NoResultFound:
            raise ObjectNotFoundException
