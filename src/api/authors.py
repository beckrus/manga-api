from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep
from src.schemas.authors import AuthorAddDTO, AuthorPatchDTO


router = APIRouter(prefix="/authors", tags=["Authors"])


@cache(expire=1)
@router.get("")
async def get_authors(filters: PaginationDep): ...


@router.post("")
async def add_author(data: AuthorAddDTO): ...


@cache(expire=1)
@router.get("/{author_id}")
async def get_author(author_id: int): ...


@router.patch("/{author_id}")
async def modify_author(author_id: int, data: AuthorPatchDTO): ...


@router.put("/{author_id}")
async def replace_author(author_id: int, data: AuthorAddDTO): ...


@router.delete("/{author_id}")
async def delete_author(author_id: int): ...
