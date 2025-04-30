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