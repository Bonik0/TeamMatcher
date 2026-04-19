from fastapi import Depends
from core.repositories.user_verification import (
    RedisUserVerificationRepository,
)
from core.dependencies.redis import get_redis_client
from redis.asyncio import Redis


def get_verification_repository(
    client: Redis = Depends(get_redis_client),
) -> RedisUserVerificationRepository:
    return RedisUserVerificationRepository(client)
