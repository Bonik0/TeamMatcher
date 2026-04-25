from pydantic import EmailStr
from uuid import UUID
from core.interfaces.repositories.user_verification import IUserVerificationRepository
from core.interfaces.use_case import IUseCase


class SaveUserVerificationUseCase(IUseCase):
    def __init__(
        self, repository: IUserVerificationRepository, lifetime_seconds: int
    ) -> None:
        self.repository = repository
        self.lifetime_seconds = lifetime_seconds

    async def execute(self, email: EmailStr, op_id: UUID) -> None:
        await self.repository.save(email, op_id, self.lifetime_seconds)
