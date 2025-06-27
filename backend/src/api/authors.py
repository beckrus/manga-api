from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.exceptions import (
    AuthorDuplicateException,
    AuthorDuplicateHTTPException,
    AuthorNotFoundException,
    AuthorNotFoundHTTPException,
)
from src.services.authors import AuthorsService
from src.api.dependencies import DBDep, get_admin_user
from src.schemas.authors import AuthorAddDTO, AuthorPatchDTO


router = APIRouter(prefix="/authors", tags=["Authors"])


@cache(expire=1)
@router.get(
    "",
    description="""
    Retrieve a list of authors from the database.

    - **name** (optional): Filter authors by name. If provided, only authors whose names match the given value will be returned.
    - **Returns**: A list of authors. If no `name` is provided, all authors will be returned.
    """,
)
async def get_authors(db: DBDep, name: str | None = None):
    return await AuthorsService(db).get_authors(name=name)


@router.post(
    "",
    description="""
    Add one or multiple authors to the database.

    - **Single Author**: Pass a dictionary with the author's details.
      Example:
      {
          "name": "Yu Aida (相田 裕)"
      }

    - **Multiple Authors**: Pass a list of dictionaries, each containing an author's details.
      Example:
      [
          {"name": "Yu Aida (相田 裕)"},
          {"name": "Koji Aihara (相原 コージ)"}
      ]

    - **Returns**: The added author(s) with their generated IDs.
    """,
    dependencies=[Depends(get_admin_user)],
)
async def add_author(db: DBDep, data: AuthorAddDTO | list[AuthorAddDTO]):
    try:
        return await AuthorsService(db).add_author(data)
    except AuthorDuplicateException:
        raise AuthorDuplicateHTTPException


@cache(expire=1)
@router.get(
    "/{author_id}",
    description="""
    Retrieve a specific author by their ID.

    - **author_id**: The ID of the author to retrieve.
    - **Returns**: The details of the author with the specified ID.
    - **Error**: Raises a 404 error if the author with the specified ID is not found.
    """,
)
async def get_author(db: DBDep, author_id: int):
    try:
        return await AuthorsService(db).get_author(author_id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException


@router.patch(
    "/{author_id}",
    description="""
    Update the details of an existing author.

    - **author_id**: The ID of the author to update.
    - **data**: A dictionary containing the fields to update. Only the provided fields will be updated.
      Example:
      {
          "name": "Updated Author Name"
      }
    - **Returns**: The updated details of the author.
    - **Error**: Raises a 404 error if the author with the specified ID is not found.
    """,
    dependencies=[Depends(get_admin_user)],
)
async def modify_author(db: DBDep, author_id: int, data: AuthorPatchDTO):
    try:
        return await AuthorsService(db).modify_author(author_id, data)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException


@router.delete(
    "/{author_id}",
    status_code=204,
    description="""
    Delete an author from the database by their ID.

    - **author_id**: The ID of the author to delete.
    - **Returns**: No content (204 status code) if the deletion is successful.
    - **Error**: Raises a 404 error if the author with the specified ID is not found.
    """,
    dependencies=[Depends(get_admin_user)],
)
async def delete_author(db: DBDep, author_id: int):
    try:
        await AuthorsService(db).delete_author(author_id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
