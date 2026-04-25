from typing import Protocol
from pydantic import EmailStr
from core.entities import VerificationCode


class IVerificationRepository(Protocol):
    async def save(
        self, verification_code: VerificationCode, lifetime_seconds: int
    ) -> None:
        pass

    async def delete(self, email: EmailStr) -> None:
        pass

    async def find_by_email(self, email: EmailStr) -> VerificationCode | None:
        pass

    async def increment_attempts(self, email: EmailStr) -> None:
        pass
