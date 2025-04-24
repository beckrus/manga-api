from pydantic import BaseModel


class MangaAddDTO(BaseModel):
    author: int
    main_name: str
    secondary_name: str | None
    description: str
    image: str | None


class MangaDBAddDTO(MangaAddDTO):
    created_by: int


class MangaResponseDTO(MangaAddDTO):
    id: int


class MangaPatchDTO(BaseModel):
    author: int | None = None
    main_name: str | None = None
    secondary_name: str | None = None
    description: str | None = None
    image: str | None = None
