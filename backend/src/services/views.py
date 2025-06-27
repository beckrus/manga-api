from src.schemas.manga import MangaIncreaseViewsDTO
from src.schemas.views import TrackingInfo
from src.exceptions import (
    FKObjectNotFoundException,
    MangaNotFoundException,
    ObjectDuplicateException,
)
from src.services.base import BaseService
from src.utils.redis_connector import redis_manager


class ViewsService(BaseService):
    async def increase_count_views(self, manga_id: int, tracking_info: TrackingInfo):
        try:
            # check redis about other tracks
            if tracking_info.user_id:
                seen_before = await redis_manager.get(f"views.{manga_id}.{tracking_info.user_id}")
                if seen_before:
                    return
                else:
                    await redis_manager.set(f"views.{manga_id}.{tracking_info.user_id}", "1")
            else:
                seen_before = await redis_manager.get(f"views.{manga_id}.{tracking_info.ip}")
                if seen_before:
                    return
                else:
                    await redis_manager.set(f"views.{manga_id}.{tracking_info.ip}", "1")
            manga = await self.db.manga.get_one_by_id(manga_id)
            patch_data = MangaIncreaseViewsDTO.model_validate(
                {"count_views": manga.count_views + 1}
            )
            await self.db.manga.edit(manga_id, patch_data, exclude_unset=True)
            await self.db.commit()
        except ObjectDuplicateException:
            pass
        except FKObjectNotFoundException as e:
            raise MangaNotFoundException from e
