from pydantic import BaseModel


class ReadProgressDTO(BaseModel):
    user_id: int
    manga_id: int
    chapter_id: int
