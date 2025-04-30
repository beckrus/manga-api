from fastapi import APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="", tags=["html"])
templates = Jinja2Templates(directory="templates")
