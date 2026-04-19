from fastapi import Depends
from core.repositories.token_black_list import RedisBlacklistRepository
from core.dependencies.redis import get_redis_client
from redis.asyncio import Redis


def get_token_blacklist_repository(
    client: Redis = Depends(get_redis_client),
) -> RedisBlacklistRepository:
    return RedisBlacklistRepository(client)
