from src.services.token import TokenService
from src.schemas.users import UserAddDTO, UserDBAddDTO, UserPatchDTO
from src.exceptions import (
    PasswordMatchException,
    UserDuplicateException,
    UserNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.services.base import BaseService
from src.tasks.email import send_welcome_email_task


class UsersService(BaseService):
    async def get_users(self):
        return await self.db.users.get_all()

    async def get_user_by_id(self, user_id: int):
        try:
            user = await self.db.users.get_one_by_id(user_id)
            if user is None:
                raise UserNotFoundException
            return user
        except ObjectNotFoundException as e:
            raise UserNotFoundException from e

    async def add_user(self, data: UserAddDTO):
        if data.password != data.password_confirm:
            raise PasswordMatchException
        data.username = (data.username).lower()
        data.email = (data.email).lower()
        password_hash = TokenService.hash_password(data.password)
        is_first_user = await self.db.users.count_users()
        try:
            user = UserDBAddDTO.model_validate(
                {**data.model_dump(), "password_hash": password_hash}
            )
            if is_first_user == 0:
                user.is_admin = True
            result = await self.db.users.add(user)
            await self.db.commit()
            send_welcome_email_task.delay(user.model_dump())
            return result
        except ObjectDuplicateException as e:
            raise UserDuplicateException from e

    async def modify_user(self, user_id: int, data: UserPatchDTO):
        if data.password or data.password_confirm and data.password != data.password_confirm:
            raise PasswordMatchException
        try:
            user = await self.db.users.edit(user_id, data=data, exclude_unset=True)
            await self.db.commit()
            return user
        except ObjectNotFoundException as e:
            raise UserNotFoundException from e

    async def delete_user(self, user_id: int):
        try:
            await self.db.users.delete(user_id)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise UserNotFoundException from e
