import logging
from core.interfaces.repositories.rate_limiter import IRateLimiterRepository


class RateLimitUseCase:
    def __init__(
        self, repository: IRateLimiterRepository, logger: logging.Logger
    ) -> None:
        self.repository = repository
        self.logger = logger

    async def allow_request(
        self, keys: list[str], limit: int, period: int, block_time: int
    ) -> tuple[bool, int]:
        is_blocked, ttl = await self.repository.is_blocked(keys)
        if is_blocked:
            self.logger.info(f"key={keys} is blocked, ttl={ttl}")
            return False, ttl

        current_count = await self.repository.increment_count(keys, period)

        if current_count >= limit:
            await self.repository.block(keys, block_time)
            await self.repository.reset_count(keys)
            self.logger.info(f"block key={keys} for {block_time}")

        self.logger.info(f"OK for key={keys}")
        return True, 0
