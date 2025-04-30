from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.exceptions import ChapterNotFoundException
from src.services.chapters import ChaptersService
from src.services.pages import PagesService
from src.api.dependencies import DBDep, MangaFilterDep, PaginationDep, get_user_or_ip
from src.services.manga import MangaService

router = APIRouter(prefix="", tags=["html"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/web/manga", response_class=HTMLResponse)
async def manga_list_partial(
    request: Request, db: DBDep, pagination: PaginationDep, filter: MangaFilterDep
):
    mangas = await MangaService(db).get_manga(filter=filter, pagination=pagination)
    return templates.TemplateResponse(
        "partials/manga_list.html", {"request": request, "mangas": mangas}
    )


@router.get("/web/manga/{manga_id}", response_class=HTMLResponse)
async def manga_detail(
    request: Request, manga_id: int, db: DBDep, tracking_info=Depends(get_user_or_ip)
):
    manga = await MangaService(db).get_manga_by_id(manga_id, tracking_info.user_id)
    chapters = await ChaptersService(db).get_chapters(manga_id)
    return templates.TemplateResponse(
        "manga_detail.html", {"request": request, "manga": manga, "chapters": chapters}
    )


@router.get("/web/manga/{manga_id}/chapters/{chapter_number}", response_class=HTMLResponse)
async def chapter_pages(
    request: Request,
    manga_id: int,
    chapter_number: int,
    db: DBDep,
    tracking_info=Depends(get_user_or_ip),
):
    try:
        chapter = await ChaptersService(db).get_chapter_by_number(chapter_number, manga_id)
    except ChapterNotFoundException:
        chapter_next = None
    try:
        chapter_next = await ChaptersService(db).get_chapter_by_number(chapter.number + 1, manga_id)
        chapter_next = chapter_next.number
    except ChapterNotFoundException:
        chapter_next = None
    pages = await PagesService(db).get_pages(chapter.id)
    return templates.TemplateResponse(
        "partials/page.html",
        {
            "number": chapter.number,
            "request": request,
            "pages": pages,
            "manga_id": manga_id,
            "chapter_id": chapter.id,
            "next_chapter_number": chapter_next,
        },
    )


@router.get("/web/manga/{manga_id}/reader", response_class=HTMLResponse)
async def reader(request: Request, manga_id: int, db: DBDep):
    try:
        chapter = await ChaptersService(db).get_chapter_by_number(1, manga_id)
    except ChapterNotFoundException:
        chapter_next = None
    try:
        chapter_next = await ChaptersService(db).get_chapter_by_number(chapter.number + 1, manga_id)
        chapter_next = chapter_next.number
    except ChapterNotFoundException:
        chapter_next = None
    pages = await PagesService(db).get_pages(chapter.id)
    return templates.TemplateResponse(
        "reader.html",
        {
            "number": chapter.number,
            "request": request,
            "pages": pages,
            "manga_id": manga_id,
            "chapter_id": chapter.id,
            "next_chapter_number": chapter_next,
        },
    )
