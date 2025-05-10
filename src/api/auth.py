from typing import Annotated
from fastapi import APIRouter, Form, Response


from config import settings
from src.exceptions import (
    GoogleAuthFailedHTTPException,
    GoogleAuthFailedUserInfoException,
    PasswordMatchException,
    PasswordMatchHTTPException,
    RefreshTokenExpiredException,
    RefreshTokenExpiredHTTPException,
    RefreshTokenNotFoundHTTPException,
    UserAuthException,
    UserAuthHTTPException,
    UserDuplicateException,
    UserDuplicateHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.services.auth import AuthService
from src.api.dependencies import DBDep, RefreshTokenDep, UserIdDep
from src.services.users import UsersService
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
    - **Returns**: Access and refresh(cookie only) tokens.
    - **Cookies**: Sets `refresh_token` as an HTTP-only cookie.
    - **Error**: Raises a 401 error if the credentials are invalid or the user is not found.
    """,
)
async def login(
    db: DBDep,
    data: Annotated[UserLoginDTO, Form()],
    response: Response,
    refresh_token: RefreshTokenDep,
):
    try:
        tokens = await AuthService(db).authenticate_user(data)
        if refresh_token:
            await AuthService(db).delete_refresh_token(refresh_token)
    except (UserAuthException, UserNotFoundException):
        raise UserAuthHTTPException

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=60 * settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        httponly=True,
    )
    return {"access_token": tokens.access_token}


@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/google")
async def auth_google(code: str, db: DBDep, response: Response):
    try:
        user_info = await AuthService(db).get_google_user_info(code)
    except GoogleAuthFailedUserInfoException:
        raise GoogleAuthFailedHTTPException

    tokens = await AuthService(db).authenticate_oauth_user(user_info)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=60 * settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        httponly=True,
    )

    return {"access_token": tokens.access_token}


@router.post(
    "/logout",
    summary="Logout User",
    description="""
    Log out the current user by deleting their authentication cookies and refresh token.

    - **Returns**: A message confirming the user has been logged out.
    """,
)
async def logout_user(db: DBDep, response: Response, refresh_token: RefreshTokenDep):
    if refresh_token:
        await AuthService(db).delete_refresh_token(refresh_token)
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.post(
    "/refresh-token",
    summary="Refresh Token",
    description="""
    Refresh the access token using a valid refresh token.

    - **Cookies**: Requires a valid `refresh_token` cookie.
    - **Returns**: A new access token and updates the `refresh_token` cookie.
    - **Error**: Raises a 404 error if the refresh token is not found or a 401 error if the refresh token has expired.
    """,
)
async def refresh_token(db: DBDep, response: Response, refresh_token: RefreshTokenDep):
    if not refresh_token:
        raise RefreshTokenNotFoundHTTPException
    try:
        tokens = await AuthService(db).refresh_token(refresh_token)
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            max_age=60 * settings.REFRESH_TOKEN_EXPIRE_MINUTES,
            httponly=True,
            secure=True,
        )

        return {"access_token": tokens.access_token}

    except RefreshTokenExpiredException:
        raise RefreshTokenExpiredHTTPException


@router.delete(
    "/refresh-token-all",
    summary="Delete All Refresh Tokens",
    description="""
    Delete all refresh tokens for the currently authenticated user.

    - **Access**: Requires the user to be authenticated.
    - **Returns**: No content (204 status code) if successful.
    """,
    status_code=204,
)
async def delete_all_users_refresh_tokens(user_id: UserIdDep, db: DBDep):
    try:
        return await AuthService(db).delete_all_tokens(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


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
        return await UsersService(db).get_one_by_id_with_rel(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
