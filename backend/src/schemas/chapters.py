from pydantic import BaseModel, Field, model_validator


class ChapterAddDTO(BaseModel):
    number: int
    is_premium: bool
    price: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_price(self):
        if self.is_premium and self.price < 0:
            return ValueError("Price must be gt 0 if chapter is premium")
        return self


class ChapterPatchDTO(ChapterAddDTO):
    number: int | None = None
    is_premium: bool | None = None
    price: int | None = Field(default=None, ge=0)


class ChapterDBAddDTO(ChapterAddDTO):
    manga_id: int
    created_by: int


class ChapterPageDTO(BaseModel):
    id: int
    number: int
    url: str


class ChapterResponseDTO(BaseModel):
    id: int
    number: int
    manga_id: int
    is_premium: bool
    price: int


class ChapterResponseWithPagesDTO(ChapterResponseDTO):
    pages: list[ChapterPageDTO]
