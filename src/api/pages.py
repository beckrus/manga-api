from fastapi import APIRouter
from fastapi_cache.decorator import cache

from api.dependencies import PaginationDep
from src.schemas.pages import PageAddDTO, PagePatchDTO


router = APIRouter(
    prefix="/manga/{manga_id}/chapters/{chapter_id}/pages", tags=["Pages"]
)


@cache(expire=1)
@router.get("")
async def get_page(filters: PaginationDep): ...


@cache(expire=1)
@router.get("/{page_id}")
async def get_page_by_id(page_id: int): ...


@router.post("/pages")
async def add_page(data: PageAddDTO): ...


@router.patch("/{page_id}")
async def modify_page(page_id: int, data: PagePatchDTO): ...


@router.put("/{page_id}")
async def replace_page(page_id: int, data: PageAddDTO): ...


@router.delete("/{page_id}")
async def delete_page(page_id: int): ...
