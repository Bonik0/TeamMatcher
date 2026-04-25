from core.repositories.rate_limiter import (
    RedisRateLimiterRepository,
)
from core.rate_limiter.use_case import RateLimitUseCase
from core.dependencies.redis import get_redis_client
import logging


def get_rate_limiter_repository() -> RedisRateLimiterRepository:
    client = get_redis_client()
    return RedisRateLimiterRepository(client)


def get_rate_limiter_use_case(logger: logging.Logger) -> RateLimitUseCase:
    repository = get_rate_limiter_repository()
    return RateLimitUseCase(repository, logger)
