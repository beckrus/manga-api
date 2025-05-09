import asyncio
from src.api.dependencies import get_db_manager_null_pull
from src.tasks.celery import celery_app


async def delete_expired_tokens():
    async with get_db_manager_null_pull() as db:
        return await db.refresh_tokens.delete_expired_tokens()


@celery_app.task()
def delete_expired_tokens_task():
    count = asyncio.run(delete_expired_tokens())
    return {"Deleted expired tokens": count}
