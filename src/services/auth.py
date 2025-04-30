from src.services.token import TokenService
from src.schemas.users import UserAddDTO, UserDBAddDTO, UserLoginDTO, UserTokens
from src.exceptions import (
    UserAuthException,
    UserDuplicateException,
    ObjectDuplicateException,
)
from src.services.base import BaseService


class AuthService(BaseService):
    async def create_user(self, data: UserAddDTO):
        password_hash = TokenService.hash_password(data.password)
        try:
            user = UserDBAddDTO.model_validate(
                {**data.model_dump(), "password_hash": password_hash}
            )
            result = await self.db.users.add(user)
            await self.db.commit()
            return result
        except ObjectDuplicateException as e:
            raise UserDuplicateException from e

    async def authenticate_user(self, data: UserLoginDTO) -> str:
        user = await self.db.users.get_one_by_name_or_email(username=data.username)
        if user and TokenService.verify_password(data.password, user.password_hash):
            access_token = TokenService.create_access_token(
                {"user_id": user.id, "username": user.username}
            )
            refresh_token = TokenService.create_refresh_token(
                {"user_id": user.id, "username": user.username}
            )
            return UserTokens.model_validate(
                {"access_token": access_token, "refresh_token": refresh_token}
            )
        raise UserAuthException
