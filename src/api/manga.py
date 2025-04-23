from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.dependencies import PaginationDep
from schemas.manga import MangaAddDTO, MangaPatchDTO


router = APIRouter(prefix="/manga", tags=["Manga"])


@cache(expire=1)
@router.get("/")
async def get_manga(filters: PaginationDep): ...


@cache(expire=1)
@router.get("/{manga_id}")
async def get_manga_by_id(manga_id: int): ...


@router.post("/")
async def add_manga(data: MangaAddDTO): ...


@router.patch("/{manga_id}")
async def modify_manga(manga_id: int, data: MangaPatchDTO): ...


@router.put("/{manga_id}")
async def replace_manga(manga_id: int, data: MangaAddDTO): ...


@router.delete("/{manga_id}")
async def delete_manga(manga_id: int): ...
