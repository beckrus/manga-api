import logging
import secrets

import httpx

from src.services.token import TokenService
from src.schemas.users import UserAddDTO, UserDBAddDTO, UserLoginDTO, UserOAuth2LoginDTO, UserTokens
from src.exceptions import (
    GoogleAuthFailedUserInfoException,
    ObjectNotFoundException,
    RefreshTokenExpiredException,
    UserAuthException,
    UserDuplicateException,
    ObjectDuplicateException,
    UserNotFoundException,
)
from src.services.base import BaseService
from src.config import settings


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

    async def authenticate_oauth_user(self, data: UserOAuth2LoginDTO) -> UserTokens:
        try:
            user = await self.db.users.get_one_by_name_or_email(username=data.email)
        except ObjectNotFoundException:
            pwd = secrets.token_urlsafe(32)
            data_add = UserAddDTO.model_validate(
                {
                    "username": data.username,
                    "email": data.email,
                    "password": pwd,
                    "password_confirm": pwd,
                }
            )
            user = await self.create_user(data_add)

        access_token = TokenService.create_access_token(
            {"user_id": user.id, "username": user.username}
        )
        refresh_token = await self.db.refresh_tokens.add_token(user.id)
        await self.db.commit()
        return UserTokens.model_validate(
            {"access_token": access_token, "refresh_token": refresh_token}
        )

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

    async def get_google_user_info(self, code: str):
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            google_response = await client.post(token_url, data=data)
            access_token = google_response.json().get("access_token")
            try:
                user_info_resp = await client.get(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                user_info = user_info_resp.json()
            except Exception:
                logging.error("Google authentication failed: unable to obtain user details\n{e}")
                raise GoogleAuthFailedUserInfoException

            user_email = user_info.get("email")
            user_name = user_info.get("name")

            if user_info.get("id") is None:
                logging.error("Google authentication failed: Account ID not found")
                raise GoogleAuthFailedUserInfoException

            return UserOAuth2LoginDTO.model_validate({"username": user_name, "email": user_email})
