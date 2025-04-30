import asyncio
import redis.asyncio as redis
from redis.exceptions import ConnectionError
import logging
from src.exceptions import RedisConnectionError
from src.config import settings


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis: redis.Redis = None

    async def connect(self, try_count: int = 1, try_max: int = 5):
        logging.info(f"Connecting to Redis server: {self.host=}, {self.port=}...")
        self.redis = redis.Redis(host=self.host, port=self.port)

        try:
            await self.redis.ping()
            logging.info("Redis connection established successfully!")
        except ConnectionError as e:
            logging.warning("Redis server did not respond to ping.")
            if try_count >= try_max:
                raise RedisConnectionError from e
            logging.info("Retry in 10s...")
            await asyncio.sleep(10)
            await self.connect(try_count=try_count + 1)

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
        logging.info("Redis connection closed")


redis_manager = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
