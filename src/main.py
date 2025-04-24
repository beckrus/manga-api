from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.authors import router as authors_router
from src.api.manga import router as manga_router
from src.api.chapters import router as chapters_router
from src.api.pages import router as pages_router
from src.api.comments import router as comments_router
from src.api.favorites import router as favorites_router


app = FastAPI(description="Manga Reader")

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(authors_router)
app.include_router(manga_router)
app.include_router(chapters_router)
app.include_router(pages_router)
app.include_router(comments_router)
app.include_router(favorites_router)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
)


reports = [
    {
        "report_name": "Gogo",
        "description": str,
        "time_from": datetime,
        "time_to": datetime,
    },
    {
        "report_name": "Yoyo",
        "recipients": str,
    },
]
