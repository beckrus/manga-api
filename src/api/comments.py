from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import CommentDuplicateException, CommentDuplicateHTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.services.comments import CommentsService
from src.schemas.comments import CommentAddDTO


router = APIRouter(prefix="/manga/{manga_id}/comments", tags=["Comments"])


@cache(expire=1)
@router.get("")
async def get_comments(db: DBDep, manga_id: int):
    return await CommentsService(db).get_comments(manga_id)


@router.post("")
async def add_comment(db: DBDep, manga_id: int, user_id: UserIdDep, data: CommentAddDTO):
    try:
        return await CommentsService(db).add_comment(manga_id, user_id, data)
    except CommentDuplicateException:
        raise CommentDuplicateHTTPException


@router.patch("/{comment_id}")
async def replace_comment(db: DBDep, comment_id: int, user_id: UserIdDep, data: CommentAddDTO):
    return await CommentsService(db).modify_comment(comment_id, user_id, data)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(db: DBDep, comment_id: int, user_id: UserIdDep):
    await CommentsService(db).delete_comment(comment_id, user_id)
