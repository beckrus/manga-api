from fastapi import APIRouter

from src.schemas.users import UserAddDTO, UserPatchDTO

router = APIRouter(prefix="/users", tags=["Users"])


# for admins only


@router.get("")
async def get_users(): ...


@router.post("")
async def add_user(data: UserAddDTO): ...


@router.patch("/{user_id}")
async def modify_user(user_id: int, data: UserPatchDTO): ...


@router.put("/{user_id}")
async def replace_user(user_id: int, data: UserAddDTO): ...


@router.delete("/{user_id}")
async def delete_user(): ...
