from redis.asyncio import Redis
from uuid import UUID
from core.interfaces.repositories.token_black_list import IBlacklistRepository


class RedisBlacklistRepository(IBlacklistRepository):
    def __init__(self, client: Redis) -> None:
        self.client = client

    def _get_device_key(self, device_id: UUID) -> str:
        return f"blacklist:device_id:{device_id}"

    def _get_user_revocation_key(self, user_id: int) -> str:
        return f"blacklist:user:{user_id}"

    async def add_device_to_blacklist(self, device_id: UUID, ttl: int) -> bool:
        key = self._get_device_key(device_id)
        await self.client.setex(key, ttl, "revoked")
        return True

    async def is_device_blacklisted(self, device_id: UUID) -> bool:
        key = self._get_device_key(device_id)
        is_exists = await self.client.exists(key)
        return is_exists == 1

    async def set_user_revocation_timestamp(
        self, user_id: int, timestamp: int, ttl: int
    ) -> None:
        key = self._get_user_revocation_key(user_id)
        await self.client.setex(key, ttl, timestamp)

    async def get_user_revocation_timestamp(self, user_id: int) -> int | None:
        key = self._get_user_revocation_key(user_id)
        value = await self.client.get(key)
        if value is None:
            return None
        return int(value)
