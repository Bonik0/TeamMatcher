from typing import Protocol


class IRateLimiterRepository(Protocol):
    async def is_blocked(self, keys: list[str]) -> tuple[bool, int]:
        pass

    async def increment_count(self, keys: list[str], period: int) -> int:
        pass

    async def block(self, keys: list[str], block_time: int) -> None:
        pass

    async def reset_count(self, keys: list[str]) -> None:
        pass
