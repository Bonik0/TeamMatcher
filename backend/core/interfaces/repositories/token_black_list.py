from typing import Protocol
from uuid import UUID


class IBlacklistRepository(Protocol):
    async def add_device_to_blacklist(self, device_id: UUID, ttl: int) -> bool:
        pass

    async def is_device_blacklisted(self, device_id: UUID) -> bool:
        pass

    async def set_user_revocation_timestamp(
        self, user_id: int, timestamp: int, ttl: int
    ) -> None:
        pass

    async def get_user_revocation_timestamp(self, user_id: int) -> int | None:
        pass
