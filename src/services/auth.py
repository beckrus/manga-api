from src.services.token import TokenService
from src.schemas.users import UserAddDTO, UserDBAddDTO, UserLoginDTO, UserTokens
from src.exceptions import (
    ObjectNotFoundException,
    RefreshTokenExpiredException,
    UserAuthException,
    UserDuplicateException,
    ObjectDuplicateException,
    UserNotFoundException,
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

    async def authenticate_user(self, data: UserLoginDTO) -> UserTokens:
        try:
            user = await self.db.users.get_one_by_name_or_email(username=data.username)
        except ObjectNotFoundException as e:
            raise UserNotFoundException from e
        if user and TokenService.verify_password(data.password, user.password_hash):
            access_token = TokenService.create_access_token(
                {"user_id": user.id, "username": user.username}
            )
            refresh_token = await self.db.refresh_tokens.add_token(user.id)
            await self.db.commit()
            return UserTokens.model_validate(
                {"access_token": access_token, "refresh_token": refresh_token}
            )
        raise UserAuthException

    async def refresh_token(self, refresh_token: str) -> UserTokens:
        token = await self.db.refresh_tokens.get_token(refresh_token)
        user = await self.db.users.get_one_by_id(id=token.user_id)
        access_token = TokenService.create_access_token(
            {"user_id": user.id, "username": user.username}
        )
        new_refresh_token = await self.db.refresh_tokens.add_token(user.id)
        await self.db.refresh_tokens.delete(token.id)
        await self.db.commit()
        return UserTokens.model_validate(
            {"access_token": access_token, "refresh_token": new_refresh_token}
        )

    async def delete_refresh_token(self, refresh_token) -> None:
        try:
            token = await self.db.refresh_tokens.get_token(refresh_token)
            await self.db.refresh_tokens.delete(token.id)
            await self.db.commit()
        except RefreshTokenExpiredException:
            pass

    async def delete_all_tokens(self, user_id: int) -> None:
        await self.db.refresh_tokens.delete_users_tokens(user_id)
