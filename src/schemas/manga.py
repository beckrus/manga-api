from pydantic import BaseModel


class MangaAddDTO(BaseModel):
    author: int
    main_name: str
    secondary_name: str | None
    description: str
    image: str | None


class MangaPatchDTO(BaseModel):
    author: int | None
    main_name: str | None
    secondary_name: str | None
    description: str | None
    image: str | None
