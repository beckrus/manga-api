from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.dependencies import PaginationDep
from src.schemas.pages import PageAddDTO, PagePatchDTO


router = APIRouter(prefix="/manga/{manga_id}/chapters", tags=["Chapters"])


@cache(expire=1)
@router.get("")
async def get_chapter(filters: PaginationDep): ...


@cache(expire=1)
@router.get("/{chapter_id}")
async def get_chapter_by_id(chapter_id: int): ...


@router.post("")
async def add_chapter(data: PageAddDTO): ...


@router.patch("/{chapter_id}")
async def modify_chapter(chapter_id: int, data: PagePatchDTO): ...


@router.put("/{chapter_id}")
async def replace_chapter(chapter_id: int, data: PageAddDTO): ...


@router.delete("/{chapter_id}")
async def delete_chapter(chapter_id: int): ...
