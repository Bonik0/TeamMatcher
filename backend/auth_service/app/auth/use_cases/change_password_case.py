import logging
from pydantic import EmailStr
from core.interfaces.repositories.user import IUserRepository
from core.interfaces.repositories.hashing import IHashingRepository
from uuid import UUID
from fastapi import HTTPException, status
from core.entities import User
from core.interfaces.repositories.user_verification import IUserVerificationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.use_case import IUseCase


class ChangePasswordUseCase(IUseCase):
    def __init__(
        self,
        repository: IUserRepository,
        hashing: IHashingRepository,
        verification: IUserVerificationRepository,
        logger: logging.Logger,
    ) -> None:
        self.repository = repository
        self.hashing = hashing
        self.verification = verification
        self.logger = logger

    async def execute(
        self,
        session: AsyncSession,
        email: EmailStr,
        operation_id: UUID,
        new_password: str,
    ) -> User:
        hashed = self.hashing.hash_password(new_password)
        user = await self.repository.get_by_email(session, email)
        is_verified = await self.verification.exist(email, operation_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {email} not found",
            )
        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="you need to pass verification in one of the ways",
            )

        await self.repository.update_password(session, email, hashed)
        await self.verification.delete(email, operation_id)
        self.logger.info(f"Password changed for {email}")
        await session.commit()
        return user
