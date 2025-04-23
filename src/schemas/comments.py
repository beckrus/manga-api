from datetime import datetime
from pydantic import BaseModel


class CommentAddDTO(BaseModel):
    text: str


class CommentResponseDTO(CommentAddDTO):
    id: int


class AuthorResponseFullDTO(CommentResponseDTO):
    user_id: int
    created_at: datetime
    modified_at: datetime
