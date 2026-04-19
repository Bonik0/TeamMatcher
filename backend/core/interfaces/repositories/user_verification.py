from typing import Protocol
from pydantic import EmailStr
from uuid import UUID


class IUserVerificationRepository(Protocol):
    async def save(self, email: EmailStr, op_id: UUID, lifetime_seconds: int) -> None:
        pass

    async def delete(self, email: EmailStr, op_id: UUID) -> bool:
        pass

    async def exist(self, email: EmailStr, op_id: UUID) -> bool:
        pass
