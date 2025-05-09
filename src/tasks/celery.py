from celery import Celery
from celery.schedules import crontab

from src.config import settings


celery_app = Celery(
    "manga_tasks",
    broker=settings.REDIS_URL,
    result_backend=settings.REDIS_URL,
    include=[
        "src.tasks.email",
        "src.tasks.tokens",
    ],
)

celery_app.conf.beat_schedule = {
    "del_expired_tokens": {
        "task": "src.tasks.tokens.delete_expired_tokens_task",
        "schedule": crontab(minute="*/60"),
    },
}
