from pydantic import BaseModel


class ChapterAddDTO(BaseModel):
    number: int
    is_premium: bool


class ChapterPatchDTO(ChapterAddDTO):
    number: int | None = None
    is_premium: bool | None = None


class ChapterDBAddDTO(ChapterAddDTO):
    manga_id: int
    created_by: int


class ChapterResponseDTO(ChapterAddDTO):
    id: int
    number: int
    manga_id: int
    is_premium: bool
    # pages: list[PageForChapterDTO]
