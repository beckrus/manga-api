from fastapi import APIRouter, Depends

from src.exceptions import (
    PasswordMatchException,
    PasswordMatchHTTPException,
    UserDuplicateException,
    UserDuplicateHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.services.users import UsersService
from src.api.dependencies import DBDep, get_admin_user
from src.schemas.users import UserAddDTO, UserPatchDTO

router = APIRouter(prefix="/users", tags=["Users"])


# for admins only


@router.get("", dependencies=[Depends(get_admin_user)])
async def get_users(db: DBDep):
    return await UsersService(db).get_users()


@router.post("", dependencies=[Depends(get_admin_user)])
async def add_user(db: DBDep, data: UserAddDTO):
    try:
        return await UsersService(db).add_user(data)
    except PasswordMatchException:
        raise PasswordMatchHTTPException
    except UserDuplicateException:
        UserDuplicateHTTPException


@router.patch("/{user_id}", dependencies=[Depends(get_admin_user)])
async def modify_user(db: DBDep, user_id: int, data: UserPatchDTO):
    try:
        return await UsersService(db).modify_user(user_id, data)
    except PasswordMatchException:
        raise PasswordMatchHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.delete("/{user_id}", status_code=204, dependencies=[Depends(get_admin_user)])
async def delete_user(db: DBDep, user_id: int):
    try:
        await UsersService(db).delete_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
