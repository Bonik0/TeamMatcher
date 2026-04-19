from pydantic import EmailStr
from uuid import UUID
from redis.asyncio import Redis
from core.interfaces.repositories.user_verification import IUserVerificationRepository


class RedisUserVerificationRepository(IUserVerificationRepository):
    def __init__(self, client: Redis) -> None:
        self.client = client

    @staticmethod
    def _get_key(email: EmailStr, op_id: UUID) -> str:
        return f"verify:{email}:{op_id}"

    async def save(self, email: EmailStr, op_id: UUID, lifetime_seconds: int) -> None:
        key = self._get_key(email, op_id)
        await self.client.set(key, 0, lifetime_seconds)

    async def delete(self, email: EmailStr, op_id: UUID) -> bool:
        key = self._get_key(email, op_id)
        deleted = await self.client.delete(key)

        return bool(deleted)

    async def exist(self, email: EmailStr, op_id: UUID) -> bool:
        key = self._get_key(email, op_id)
        is_exist = await self.client.exists(key)
        return bool(is_exist)
