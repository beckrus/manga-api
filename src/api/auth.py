from fastapi import APIRouter

from src.schemas.users import UserAddDTO

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/")
async def register(data: UserAddDTO): ...


@router.post("/login")
async def login(): ...


@router.post("/logout")
async def logout(): ...


@router.get("/me")
async def about_me(): ...
