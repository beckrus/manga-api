from pydantic import BaseModel

from src.schemas.pages import PageForChapterDTO


class ChapterAddDTO(BaseModel):
    number: int
    manga_id: str
    is_premium: bool


class ChapterPatchDTO(BaseModel):
    number: int | None
    url: str | None

class ChapterAddDTO(ChapterAddDTO):
    number: int
    manga_id: str
    is_premium: bool
    pages: list[PageForChapterDTO]