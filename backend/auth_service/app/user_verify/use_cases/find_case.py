from pydantic import EmailStr
from uuid import UUID
from core.interfaces.repositories.user_verification import IUserVerificationRepository
from core.interfaces.use_case import IUseCase


class FindUserVerificationUseCase(IUseCase):
    def __init__(self, repository: IUserVerificationRepository) -> None:
        self.repository = repository

    async def execute(self, email: EmailStr, op_id: UUID) -> bool:
        return await self.repository.exist(email, op_id)
