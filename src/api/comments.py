from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.schemas.comments import CommentAddDTO


router = APIRouter(prefix="/manga/{manga_id}/comments", tags=["Comments"])


@cache(expire=1)
@router.get("")
async def get_comments(manga_id: int):
    return manga_id


@router.post("")
async def add_comment(data: CommentAddDTO): ...


@router.put("/{comment_id}")
async def replace_comment(comment_id: int, data: CommentAddDTO): ...


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int): ...
