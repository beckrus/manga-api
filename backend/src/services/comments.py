from src.schemas.comments import CommentAddDTO, CommentDBAddDTO
from src.exceptions import (
    AccessForbiddenException,
    CommentDuplicateException,
    CommentNotFoundException,
    MangaNotFoundException,
    FKObjectNotFoundException,
    ObjectDuplicateException,
    ObjectNotFoundException,
)
from src.services.base import BaseService


class CommentsService(BaseService):
    async def get_comments(self, manga_id: int):
        return await self.db.comments.get_filtered(manga_id=manga_id)

    async def add_comment(self, manga_id: int, user_id: int, data: CommentAddDTO):
        try:
            comment = CommentDBAddDTO.model_validate(
                {"manga_id": manga_id, "user_id": user_id, "text": data.text}
            )
            comment = await self.db.comments.add(comment)
            await self.db.commit()
            return comment
        except FKObjectNotFoundException as e:
            raise MangaNotFoundException from e
        except ObjectDuplicateException as e:
            raise CommentDuplicateException from e

    async def modify_comment(self, comment_id: int, user_id: int, data: CommentAddDTO):
        try:
            user = await self.db.users.get_one_by_id(user_id)
            comment = await self.db.comments.get_one_by_id(comment_id)

            if user.id != comment.user_id and not user.is_admin:
                raise AccessForbiddenException

            comment = await self.db.comments.edit(comment.id, data=data, exclude_unset=True)
            await self.db.commit()

            return comment

        except ObjectNotFoundException as e:
            raise CommentNotFoundException from e

    async def delete_comment(self, comment_id: int, user_id: int):
        try:
            comment = await self.db.comments.get_one_by_id(comment_id)
            user = await self.db.users.get_one_by_id(user_id)

            if user.id != comment.user_id and not user.is_admin:
                raise AccessForbiddenException

            await self.db.comments.delete(id=comment_id)
            await self.db.commit()
        except ObjectNotFoundException as e:
            raise CommentNotFoundException from e
