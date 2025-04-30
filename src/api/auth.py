from typing import Annotated
from fastapi import APIRouter, Form, Response

from config import settings
from src.exceptions import (
    PasswordMatchException,
    PasswordMatchHTTPException,
    UserAuthException,
    UserAuthHTTPException,
    UserDuplicateException,
    UserDuplicateHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.services.auth import AuthService
from src.api.dependencies import DBDep, UserIdDep
from services.users import UsersService
from src.schemas.users import UserAddDTO, UserLoginDTO

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    description="""
    Register a new user.

    - **data**: The user details for registration.
      Example:
      {
          "username": "new_user",
          "email": "user@example.com",
          "password": "securepassword"
          "password_confirm": "securepassword"
      }
    - **Returns**: The details of the newly registered user.
    - **Error**: Raises a 409 error if the user already exists.
    - ** First user will be is_admin
    """,
)
async def register(db: DBDep, data: UserAddDTO):
    try:
        return await UsersService(db).add_user(data)
    except PasswordMatchException:
        raise PasswordMatchHTTPException
    except UserDuplicateException:
        raise UserDuplicateHTTPException


@router.post(
    "/login",
    description="""
    Authenticate a user and return access and refresh tokens.

    - **data**: The login credentials.
      Example:
      {
          "username": "existing_user",
          "password": "securepassword"
      }
    - **Returns**: Access and refresh tokens.
    - **Cookies**: Sets `access_token` and `refresh_token` as HTTP-only cookies.
    - **Error**: Raises a 401 error if the credentials are invalid.
    """,
)
async def login(db: DBDep, data: Annotated[UserLoginDTO, Form()], response: Response):
    try:
        tokens = await AuthService(db).authenticate_user(data)
    except UserAuthException:
        raise UserAuthHTTPException
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=60 * settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        httponly=True,
    )
    return tokens


@router.post(
    "/logout",
    summary="Logout User",
    description="""
    Log out the current user by deleting their authentication cookies.

    - **Returns**: A message confirming the user has been logged out.
    """,
)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.get(
    "/me",
    summary="Get Current User",
    description="""
    Retrieve the details of the currently authenticated user.

    - **Returns**: The details of the authenticated user.
    - **Error**: Raises a 404 error if the user is not found.
    """,
)
async def get_me(user_id: UserIdDep, db: DBDep):
    try:
        return await UsersService(db).get_user_by_id(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
