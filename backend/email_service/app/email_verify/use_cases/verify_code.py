from uuid import UUID
from pydantic import PositiveInt, EmailStr
from core.entities import VerificationCode
from core.interfaces.repositories.verification_code import IVerificationRepository
from fastapi.exceptions import HTTPException
from fastapi import status
from core.interfaces.use_case import IUseCase


class VerifyCodeUseCase(IUseCase):
    def __init__(self, repository: IVerificationRepository, max_attempts: int) -> None:
        self.repository = repository
        self.max_attempts = max_attempts

    async def execute(
        self, email: EmailStr, code: PositiveInt, operation_id: UUID
    ) -> tuple[bool, VerificationCode]:
        verification_code = await self.repository.find_by_email(email)

        if verification_code is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No verification code found for email: {email}",
            )

        if verification_code.has_exceeded_attempts(self.max_attempts):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Max attempts exceeded for email: {email}",
            )

        if verification_code.operation_id != operation_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid operation ID for email: {email}",
            )

        if verification_code.code == code:
            return True, verification_code

        await self.repository.increment_attempts(email)
        return False, verification_code
