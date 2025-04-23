from fastapi import APIRouter

from schemas.favorites import FavoriteAddDTO

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("")
async def add_rate(data: FavoriteAddDTO): ...


@router.delete("")
async def delete_rate(manga_id: int): ...
