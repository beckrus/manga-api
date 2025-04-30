from pydantic import BaseModel


class PageAddDTO(BaseModel):
    number: int
    url: str


class PagePatchDTO(BaseModel):
    number: int | None
    url: str | None


class PageDBAddDTO(PageAddDTO):
    chapter_id: int
    created_by: int


class PageForChapterDTO(BaseModel):
    number: int
    url: str


class PageResponseDTO(PageDBAddDTO):
    id: int
