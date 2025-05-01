from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="", tags=["html"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def manga_list(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/web/manga")
async def manga(manga_id: int, request: Request):
    return templates.TemplateResponse(
        "manga_detail.html", {"request": request, "manga_id": manga_id}
    )


@router.get("/web/reader")
async def reader(manga_id: int, chapter_id: int, request: Request):
    return templates.TemplateResponse(
        "reader.html", {"request": request, "manga_id": manga_id, "chapter_id": chapter_id}
    )
