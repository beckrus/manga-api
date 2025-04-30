import logging
from pathlib import Path
import sys

from fastapi.concurrency import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.append(str(Path(__file__).parent.parent))


from src.utils.redis_connector import redis_manager
from src.api.auth import router as auth_router
from src.api.users import router as users_router
from src.api.authors import router as authors_router
from src.api.manga import router as manga_router
from src.api.chapters import router as chapters_router
from src.api.pages import router as pages_router
from src.api.comments import router as comments_router
from src.api.favorites import router as favorites_router
from src.api.html import router as html_router
from src.api.purchases_chapters import router as router_purchases

FORMAT = "%(asctime)s::%(levelname)s::%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%d/%m/%Y %I:%M:%S")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("enter lifespan")
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    logging.info("exit lifespan")


app = FastAPI(description="Manga Reader", lifespan=lifespan)

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(authors_router)
app.include_router(manga_router)
app.include_router(chapters_router)
app.include_router(pages_router)
app.include_router(comments_router)
app.include_router(favorites_router)
app.include_router(html_router)
app.include_router(router_purchases)


app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
)
