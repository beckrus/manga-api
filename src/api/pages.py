from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.services.pages import PagesService
from src.api.dependencies import DBDep
from src.schemas.pages import PageAddDTO, PagePatchDTO


router = APIRouter(prefix="/manga/{manga_id}/chapters/{chapter_id}/pages", tags=["Pages"])


@cache(expire=1)
@router.get("")
async def get_page(db: DBDep, chapter_id: int):
    return await PagesService(db).get_pages(chapter_id)


@cache(expire=1)
@router.get("/{page_id}")
async def get_page_by_id(db: DBDep, chapter_id: int):
    return await PagesService(db).get_page_by_id(chapter_id)


@router.post("")
async def add_page(db: DBDep, chapter_id: int, data: PageAddDTO, user_id: int = 1):
    return await PagesService(db).add_page(chapter_id, 1, data.number, data.url)


@router.patch("/{page_id}")
async def modify_page(db: DBDep, chapter_id: int, data: PagePatchDTO):
    return await PagesService(db).modify_page(chapter_id, data)


@router.delete("/{page_id}")
async def delete_page(db: DBDep, page_id: int):
    return await PagesService(db).delete_page(page_id)
