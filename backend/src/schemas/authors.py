from datetime import datetime
from pydantic import BaseModel


class AuthorAddDTO(BaseModel):
    name: str


class AuthorResponseDTO(AuthorAddDTO):
    id: int


class AuthorResponseFullDTO(AuthorResponseDTO):
    created_at: datetime
    modified_at: datetime


class AuthorPatchDTO(BaseModel):
    name: str | None
