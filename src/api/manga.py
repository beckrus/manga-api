from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_cache.decorator import cache

from src.exceptions import (
    AuthorNotFoundException,
    AuthorNotFoundHTTPException,
    BadImageFileExtException,
    BadImageFileExtHTTPException,
    MangaDuplicateException,
    MangaDuplicateHTTPException,
    MangaNotFoundException,
    MangaNotFoundHTTPException,
)
from src.services.manga import MangaService
from src.api.dependencies import (
    DBDep,
    MangaFilterDep,
    PaginationDep,
    UserIdAdminDep,
    get_admin_user,
    get_user_or_ip,
)
from schemas.manga import MangaAddDTO, MangaPatchDTO


router = APIRouter(prefix="/manga", tags=["Manga"])


# @cache(expire=1)
@router.get(
    "",
    description="""
    Retrieve a list of manga from the database with optional filters.

    - **Filters**:
        - **name** (optional): Filter manga by their main or secondary name. Partial matches are allowed (case-insensitive).
        - **author** (optional): Filter manga by the author's name. Partial matches are allowed (case-insensitive).

    - **Pagination**:
        - **page**: The page number to retrieve, starting from 1.
        - **per_page**: The number of items to display per page (1-100).

    - **Sorting**:
        - **sort**: Sort items by name in ascending (ASC) or descending (DESC) order.

    - **Returns**: A list of manga that match the specified filters and pagination settings.

    - **Notes**:
        - If both `name` and `author` are provided, the results will include manga that match either filter.
        - If no filters are provided, all manga will be retrieved (up to the specified limit and offset).
    """,
)
async def get_manga(db: DBDep, pagination: PaginationDep, filter: MangaFilterDep):
    return await MangaService(db).get_manga(filter=filter, pagination=pagination)


@cache(expire=1)
@router.get("/{manga_id}")
async def get_manga_by_id(db: DBDep, manga_id: int, tracking_info=Depends(get_user_or_ip)):
    try:
        return await MangaService(db).get_manga_by_id(manga_id, tracking_info.user_id)
    except MangaNotFoundException:
        raise MangaNotFoundHTTPException


@router.post("")
async def add_manga(db: DBDep, data: MangaAddDTO | list[MangaAddDTO], user_id: UserIdAdminDep):
    try:
        return await MangaService(db).add_manga(user_id, data)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    except MangaDuplicateException:
        raise MangaDuplicateHTTPException


@router.post("/{manga_id}/poster")
async def add_manga_poster(
    db: DBDep, manga_id: int, user_id: UserIdAdminDep, image: Annotated[UploadFile, File()]
):
    try:
        return await MangaService(db).add_manga_poster(manga_id, image)
    except BadImageFileExtException:
        raise BadImageFileExtHTTPException
    except MangaDuplicateException:
        raise MangaDuplicateHTTPException


@router.patch("/{manga_id}", dependencies=[Depends(get_admin_user)])
async def modify_manga(db: DBDep, manga_id: int, data: MangaPatchDTO):
    try:
        return await MangaService(db).modify_manga(manga_id, data)
    except MangaNotFoundException:
        raise MangaNotFoundHTTPException


@router.delete("/{manga_id}", status_code=204, dependencies=[Depends(get_admin_user)])
async def delete_manga(db: DBDep, manga_id: int):
    try:
        return await MangaService(db).delete_manga(manga_id)
    except MangaNotFoundException:
        raise MangaNotFoundHTTPException
