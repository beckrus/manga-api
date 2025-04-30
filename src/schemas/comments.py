from datetime import datetime
from pydantic import BaseModel


class CommentUserDTO(BaseModel):
    username: str


class CommentAddDTO(BaseModel):
    text: str


class CommentDBAddDTO(CommentAddDTO):
    manga_id: int
    user_id: int
    text: str


class CommentResponseDTO(CommentDBAddDTO):
    id: int


class CommentsResponseFullDTO(CommentResponseDTO):
    user: CommentUserDTO
    created_at: datetime
    modified_at: datetime
