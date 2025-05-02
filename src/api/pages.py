from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.schemas.views import TrackingInfo
from src.exceptions import (
    ChapterIsNotPurchasedException,
    ChapterIsNotPurchasedHTTPException,
    ChapterNotFoundException,
    ChapterNotFoundHTTPException,
    PageDuplicateException,
    PageDuplicateHTTPException,
    PageNotFoundException,
    PageNotFoundHTTPException,
)
from src.services.pages import PagesService
from src.api.dependencies import DBDep, get_admin_user, get_user_or_ip
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
async def get_page(
    db: DBDep, chapter_id: int, tracking_info: TrackingInfo = Depends(get_user_or_ip)
):
    try:
        return await PagesService(db).get_pages(chapter_id, tracking_info.user_id)
    except ChapterIsNotPurchasedException:
        raise ChapterIsNotPurchasedHTTPException
    except ChapterNotFoundException:
        raise ChapterNotFoundHTTPException


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
    try:
        return await PagesService(db).get_page_by_id(chapter_id, page_id)
    except PageNotFoundException:
        raise PageNotFoundHTTPException


@router.post("", dependencies=[Depends(get_admin_user)])
async def add_page(db: DBDep, chapter_id: int, data: PageAddDTO, user_id: int = 1):
    try:
        return await PagesService(db).add_page(chapter_id, user_id, data.number, data.url)
    except ChapterNotFoundException:
        raise ChapterNotFoundHTTPException
    except PageDuplicateException:
        raise PageDuplicateHTTPException


@router.patch("/{page_id}", dependencies=[Depends(get_admin_user)])
async def modify_page(db: DBDep, page_id: int, data: PagePatchDTO):
    try:
        return await PagesService(db).modify_page(page_id, data)
    except PageNotFoundException:
        raise PageNotFoundHTTPException
    except PageDuplicateException:
        raise PageDuplicateHTTPException


@router.delete("/{page_id}", dependencies=[Depends(get_admin_user)])
async def delete_page(db: DBDep, page_id: int):
    try:
        return await PagesService(db).delete_page(page_id)
    except PageNotFoundException:
        raise PageNotFoundHTTPException
