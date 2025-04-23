from pydantic import BaseModel


class FavoriteAddDTO(BaseModel):
    user_id: int
    manga_id: int
