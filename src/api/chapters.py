from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi_cache.decorator import cache

from src.services.read_progress import ReadProgresService
from src.services.views import ViewsService
from src.services.pages import PagesService
from src.exceptions import (
    BadFileExtException,
    BadFileExtHTTPException,
    BadFileExtInArchiveException,
    BadFileExtInArchiveHTTPException,
    ChapterDuplicateException,
    ChapterDuplicateHTTPException,
    ChapterNotFoundException,
    ChapterNotFoundHTTPException,
    MangaNotFoundException,
    MangaNotFoundHTTPException,
    PageFileImageNameException,
    PageFileImageNameHTTPException,
)
from src.services.chapters import ChaptersService
from src.api.dependencies import DBDep, UserIdAdminDep, get_admin_user, get_user_or_ip
from src.schemas.chapters import ChapterAddDTO, ChapterPatchDTO, ChapterResponseDTO
from src.utils.check_file import file_inspection, rm_chapter_files, rm_file, save_page_files


router = APIRouter(prefix="/manga/{manga_id}/chapters", tags=["Chapters"])


@cache(expire=1)
@router.get(
    "",
    description="""
    Retrieve a list of chapters for a specific manga.

    - **manga_id**: The ID of the manga whose chapters are to be retrieved.
    - **Returns**: A list of chapters belonging to the specified manga.
    """,
)
async def get_chapters(db: DBDep, manga_id: int):
    return await ChaptersService(db).get_chapters(manga_id=manga_id)


@cache(expire=1)
@router.get(
    "/{chapter_id}",
    description="""
    Retrieve a specific chapter by its ID.

    - **chapter_id**: The ID of the chapter to retrieve.
    - **Returns**: The details of the chapter with the specified ID.
    - **Error**: Raises a 404 error if the chapter with the specified ID is not found.
    """,
)
async def get_chapter_by_id(db: DBDep, chapter_id: int, tracking_info=Depends(get_user_or_ip)):
    try:
        chapter = await ChaptersService(db).get_chapter_by_id(chapter_id)
        await ViewsService(db).increase_count_views(chapter.manga_id, tracking_info)
        await ReadProgresService(db).add_progress(chapter.manga_id, chapter_id, tracking_info)
        return chapter
    except ChapterNotFoundException:
        raise ChapterNotFoundHTTPException


@router.post(
    "",
    description="""
    Add one or multiple chapters to a manga.

    - **data**: A single chapter or a list of chapters to be added.
      Example for a single chapter:
      {
          "number": 1,
          "manga_id": 123,
          "is_premium": false
      }
    - **Returns**: The added chapter(s) with their generated IDs.
    """,
)
async def add_chapter(
    db: DBDep,
    manga_id: int,
    number: Annotated[int, Form(ge=0)],
    price: Annotated[int, Form(ge=0)],
    is_premium: Annotated[bool, Form()],
    file: Annotated[UploadFile, File()],
    user_id: UserIdAdminDep,
) -> ChapterResponseDTO:
    chapter_data = ChapterAddDTO(number=number, is_premium=is_premium, price=price)
    try:
        file_path = file_inspection(file)

        chapter = await ChaptersService(db).add_chapter(
            manga_id=manga_id, user_id=user_id, data=chapter_data
        )

        chapter_id = chapter.id
        pages_path = save_page_files(manga_id, chapter_id, file_path)
        for k, v in enumerate(pages_path):
            await PagesService(db).add_page(
                chapter_id=chapter_id, user_id=user_id, number=k + 1, url=v
            )
        await db.commit()
        return chapter
    except MangaNotFoundException:
        raise MangaNotFoundHTTPException
    except ChapterDuplicateException:
        raise ChapterDuplicateHTTPException
    except BadFileExtException:
        BadFileExtHTTPException
    except BadFileExtInArchiveException:
        raise BadFileExtInArchiveHTTPException
    except PageFileImageNameException:
        PageFileImageNameHTTPException
    finally:
        rm_file(file_path)


@router.patch(
    "/{chapter_id}",
    description="""
    Update specific fields of an existing chapter.

    - **chapter_id**: The ID of the chapter to update.
    - **data**: A dictionary containing the fields to update. Only the provided fields will be updated.
      Example:
      {
          "number": 2,
          "url": "https://example.com/new-chapter-url"
      }
    - **Returns**: The updated details of the chapter.
    - **Error**: Raises a 404 error if the chapter with the specified ID is not found.
    """,
    dependencies=[Depends(get_admin_user)],
)
async def modify_chapter(db: DBDep, manga_id: int, chapter_id: int, data: ChapterPatchDTO):
    try:
        return await ChaptersService(db).modify_chapter(chapter_id=chapter_id, data=data)

    except ChapterNotFoundException:
        raise ChapterNotFoundHTTPException


@router.delete(
    "/{chapter_id}",
    description="""
    Delete a specific chapter by its ID.

    - **chapter_id**: The ID of the chapter to delete.
    - **Returns**: No content (204 status code) if the deletion is successful.
    - **Error**: Raises a 404 error if the chapter with the specified ID is not found.
    """,
    status_code=204,
    dependencies=[Depends(get_admin_user)],
)
async def delete_chapter(db: DBDep, manga_id: int, chapter_id: int):
    try:
        rm_chapter_files(manga_id, chapter_id)
        return await ChaptersService(db).delete_chapter(chapter_id)
    except ChapterNotFoundException:
        raise ChapterNotFoundHTTPException
