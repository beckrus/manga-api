from pydantic import BaseModel


class PageAddDTO(BaseModel):
    number: int
    url: str
    chapter_id: int


class PagePatchDTO(BaseModel):
    number: int | None
    url: str | None

class PageForChapterDTO(BaseModel):
    number: int
    url: str