from celery import Celery
from src.config import settings


celery_app = Celery(
    "manga_tasks",
    broker=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    include=[
        "src.tasks.email",
    ],
)
