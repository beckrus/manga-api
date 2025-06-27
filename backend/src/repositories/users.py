from sqlalchemy import func, or_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundException
from src.schemas.users import UserHashedPwdDTO, UserResponseDTOwithRel
from src.models.users import UserOrm
from src.repositories.mappers.mappers import UserMapper
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserOrm
    mapper = UserMapper

    async def get_one_by_id_with_rel(self, id: int):
        try:
            query = (
                select(self.model).filter_by(id=id).options(selectinload(UserOrm.favorite_manga))
            )
            result = await self.session.execute(query)
            data = result.scalars().one()
            return UserResponseDTOwithRel.model_validate(data, from_attributes=True)
        except NoResultFound as e:
            raise ObjectNotFoundException from e

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
        except NoResultFound as e:
            raise ObjectNotFoundException from e
