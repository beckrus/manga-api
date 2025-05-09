from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwt import InvalidTokenError

from schemas.views import TrackingInfo
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        if token:
            token_data = TokenService().decode_token(token)
        return token_data["user_id"]
    except InvalidTokenError:
        raise TokenErrorHttpException


def get_refresh_token(request: Request) -> str:
    return request.cookies.get("refresh_token")


async def get_user_or_ip(request: Request) -> TrackingInfo:
    authorization = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    user_id = None
    if token:
        token_data = TokenService().decode_token(token)
        user_id = token_data["user_id"]
    ip = request.client.host

    return TrackingInfo.model_validate({"ip": ip, "user_id": user_id})


async def get_admin_user(db: DBDep, user_id: int = Depends(get_current_user)) -> int:
    user = await UsersService(db).get_user_by_id(user_id)
    if not user.is_admin:
        raise AccessForbiddenHttpException
    return user_id


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]

UserIdDep = Annotated[int, Depends(get_current_user)]

UserIdAdminDep = Annotated[int, Depends(get_admin_user)]
