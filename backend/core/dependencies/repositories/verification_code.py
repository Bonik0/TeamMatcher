from core.repositories.verification_code import (
    RedisVerificationRepository,
)
from core.dependencies.redis import get_redis_client
from fastapi import Depends
from redis import Redis


def get_verification_code_reposirory(
    client: Redis = Depends(get_redis_client),
) -> RedisVerificationRepository:
    return RedisVerificationRepository(client)
