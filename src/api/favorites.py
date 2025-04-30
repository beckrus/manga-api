from fastapi import APIRouter, Form

from src.exceptions import (
    FavoriteDuplicateException,
    FavoriteDuplicateHTTPException,
    FavoriteNotFoundException,
    FavoriteNotFoundHttpException,
    MangaNotFoundException,
    MangaNotFoundHTTPException,
)
from src.services.favorites import FavoritesService
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.get("", status_code=200)
async def get_favorites(db: DBDep, user_id: UserIdDep):
    return await FavoritesService(db).get_favorites(user_id)


@router.post("", status_code=204)
async def add_favorite(db: DBDep, user_id: UserIdDep, manga_id: int = Form()):
    try:
        return await FavoritesService(db).add_to_favorite(manga_id, user_id)
    except FavoriteDuplicateException:
        raise FavoriteDuplicateHTTPException
    except MangaNotFoundException:
        raise MangaNotFoundHTTPException


@router.delete("", status_code=204)
async def delete_favorite(db: DBDep, user_id: UserIdDep, manga_id: int = Form()):
    try:
        return await FavoritesService(db).delete_favorite(manga_id, user_id)
    except FavoriteNotFoundException:
        raise FavoriteNotFoundHttpException
