from pydantic import BaseModel


class FavoriteMangaDTO(BaseModel):
    user_id: int
    manga_id: int


class FavoriteResponseMangaDTO(BaseModel):
    id: int
    user_id: int
    manga_id: int
