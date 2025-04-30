from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.services.pages import PagesService
from src.api.dependencies import DBDep, get_admin_user
from src.schemas.pages import PageAddDTO, PagePatchDTO


router = APIRouter(prefix="/manga/{manga_id}/chapters/{chapter_id}/pages", tags=["Pages"])


@cache(expire=1)
@router.get(
    "",
    description="""
    Retrieve a list of pages for a specific chapter.

    - **chapter_id**: The ID of the chapter whose pages are to be retrieved.
    - **Returns**: A list of pages belonging to the specified chapter.
    """,
)
async def get_page(db: DBDep, chapter_id: int):
    return await PagesService(db).get_pages(chapter_id)


@cache(expire=1)
@router.get(
    "/{page_id}",
    description="""
    Retrieve a specific page by its ID.

    - **chapter_id**: The ID of the chapter to which the page belongs.
    - **page_id**: The ID of the page to retrieve.
    - **Returns**: The details of the page with the specified ID.
    """,
)
async def get_page_by_id(db: DBDep, chapter_id: int, page_id: int):
    return await PagesService(db).get_page_by_id(chapter_id, page_id)


@router.post("", dependencies=[Depends(get_admin_user)])
async def add_page(db: DBDep, chapter_id: int, data: PageAddDTO, user_id: int = 1):
    return await PagesService(db).add_page(chapter_id, user_id, data.number, data.url)


@router.patch("/{page_id}", dependencies=[Depends(get_admin_user)])
async def modify_page(db: DBDep, chapter_id: int, data: PagePatchDTO):
    return await PagesService(db).modify_page(chapter_id, data)


@router.delete("/{page_id}", dependencies=[Depends(get_admin_user)])
async def delete_page(db: DBDep, page_id: int):
    return await PagesService(db).delete_page(page_id)
