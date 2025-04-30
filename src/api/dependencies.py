import logging
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from schemas.views import TrackingInfo
from src.config import settings
from src.services.users import UsersService
from src.exceptions import (
    AccessForbiddenHttpException,
    TokenErrorHttpException,
)
from src.services.token import TokenService
from src.schemas.filters import MangaFilterSchema, PaginationParamsSchema
from src.utils.db_manager import DBManager
from src.database import async_session_maker, async_session_maker_null_pool

PaginationDep = Annotated[PaginationParamsSchema, Depends()]

MangaFilterDep = Annotated[MangaFilterSchema, Depends()]


def get_db_manager() -> DBManager:
    return DBManager(session_factory=async_session_maker)


def get_db_manager_null_pull() -> DBManager:
    return DBManager(session_factory=async_session_maker_null_pool)


async def get_db() -> AsyncGenerator[DBManager, Any]:
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str, auto_error: bool = True):
        super().__init__(tokenUrl=tokenUrl, auto_error=auto_error)

    async def __call__(self, request: Request):
        token = request.cookies.get("access_token")
        refresh = request.cookies.get("refresh_token")
        if not token and not refresh:
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Not authenticated, missing token")
            else:
                return None
        return {"access_token": token, "refresh_token": refresh}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/login")


def get_current_user(response: Response, tokens: str = Depends(oauth2_scheme)) -> int:
    token = tokens["access_token"]
    refresh = tokens["refresh_token"]
    try:
        if token:
            token_data = TokenService().decode_token(token)
        else:
            token_data = TokenService().decode_token(refresh)
            access_token = TokenService.create_access_token(
                {"user_id": token_data["user_id"], "username": token_data["username"]}
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                httponly=True,
            )
            logging.info(
                f"access_token generated via refresh_token for user {token_data['username']}"
            )
        return token_data["user_id"]
    except InvalidTokenError:
        raise TokenErrorHttpException


async def get_user_or_ip(request: Request) -> TrackingInfo:
    token = request.cookies.get("access_token")
    user_id = None
    if token:
        token_data = TokenService().decode_token(token)
        user_id = token_data["user_id"]
    refresh = request.cookies.get("refresh_token")
    if refresh:
        token_data = TokenService().decode_token(refresh)
        user_id = token_data["user_id"]
    ip = request.client.host

    return TrackingInfo.model_validate({"ip": ip, "user_id": user_id})


async def get_admin_user(db: DBDep, user_id: int = Depends(get_current_user)) -> int:
    user = await UsersService(db).get_user_by_id(user_id)
    if not user.is_admin:
        raise AccessForbiddenHttpException
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user)]

UserIdAdminDep = Annotated[int, Depends(get_admin_user)]
