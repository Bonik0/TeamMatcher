from redis.asyncio import Redis
from core.models.redis.config import get_redis_settings


redis_settings = get_redis_settings()

client = Redis(
    host=redis_settings.HOST,
    port=redis_settings.PORT,
    password=redis_settings.PASSWORD,
    db=redis_settings.DB,
)
