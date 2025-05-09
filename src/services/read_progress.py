from src.schemas.views import TrackingInfo
from src.schemas.read_progress import ReadProgressDTO
from src.exceptions import (
    FKObjectNotFoundException,
    MangaNotFoundException,
)
from src.services.base import BaseService


class ReadProgresService(BaseService):
    async def add_progress(self, manga_id: int, chapter_id: int, tracking_info: TrackingInfo):
        try:
            if tracking_info.user_id:
                data = ReadProgressDTO.model_validate(
                    {
                        "manga_id": manga_id,
                        "user_id": tracking_info.user_id,
                        "chapter_id": chapter_id,
                    }
                )
                await self.db.read_progress.add(data)
                await self.db.commit()
        except FKObjectNotFoundException as e:
            raise MangaNotFoundException from e
