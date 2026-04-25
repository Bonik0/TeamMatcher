from redis.asyncio import Redis
from core.interfaces.repositories.rate_limiter import IRateLimiterRepository


class RedisRateLimiterRepository(IRateLimiterRepository):
    def __init__(self, client: Redis) -> None:
        self.client = client

    def _get_block_key(self, keys: list[str]) -> str:
        return ":".join(["rate_limit"] + keys + ["blocked"])

    def _get_count_key(self, keys: list[str]) -> str:
        return ":".join(["rate_limit"] + keys + ["count"])

    async def is_blocked(self, keys: list[str]) -> tuple[bool, int]:
        block_key = self._get_block_key(keys)
        return await self.client.exists(block_key) == 1, await self.client.ttl(
            block_key
        )

    async def increment_count(self, keys: list[str], period: int) -> int:
        count_key = self._get_count_key(keys)
        attempt = await self.client.incr(count_key)
        if attempt == 1:
            await self.client.expire(count_key, period)
        return attempt

    async def block(self, keys: list[str], block_time: int) -> None:
        block_key = self._get_block_key(keys)
        await self.client.setex(block_key, block_time, 1)

    async def reset_count(self, keys: list[str]) -> None:
        count_key = self._get_count_key(keys)
        await self.client.delete(count_key)
