import logging
import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self) -> None:
        self.client = None

    async def connect(self) -> None:
        try:
            self.client = aioredis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
            await self.client.ping()
            logger.info("Redis connected.")
        except Exception as e:
            logger.warning("Redis unavailable: %s", e)
            self.client = None

    async def close(self) -> None:
        if self.client is not None:
            try:
                await self.client.close()
            except Exception:
                pass


redis_manager = RedisManager()
