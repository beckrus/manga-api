from fastapi import APIRouter, Form

from src.services.purchases_chapters import PurchasesChaptersService
from src.exceptions import (
    ChapterIsFreeException,
    ChapterIsFreeHTTPException,
    ChapterNotFoundException,
    ChapterNotFoundHTTPException,
    NotEnoughtCoinsException,
    NotEnoughtCoinsHTTPException,
    PurchasesChapterDuplicateException,
    PurchasesChapterDuplicateHTTPException,
)
from src.api.dependencies import DBDep, UserIdAdminDep, UserIdDep

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.get("", status_code=200)
async def get_all_purchases(db: DBDep, user_id: UserIdAdminDep):
    return await PurchasesChaptersService(db).all_purchases()


@router.get("/me", status_code=200)
async def get_my_purchases(db: DBDep, user_id: UserIdDep):
    return await PurchasesChaptersService(db).my_purchases(user_id)


@router.post("", status_code=204)
async def purchase_chapter(db: DBDep, user_id: UserIdDep, chapter_id: int = Form()):
    try:
        return await PurchasesChaptersService(db).purchase_chapter(user_id, chapter_id)
    except ChapterIsFreeException:
        raise ChapterIsFreeHTTPException
    except NotEnoughtCoinsException:
        raise NotEnoughtCoinsHTTPException
    except PurchasesChapterDuplicateException:
        raise PurchasesChapterDuplicateHTTPException
    except ChapterNotFoundException:
        raise ChapterNotFoundHTTPException
