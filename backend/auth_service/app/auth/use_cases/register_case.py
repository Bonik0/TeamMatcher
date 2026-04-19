import logging
from core.interfaces.repositories.user import IUserRepository
from core.interfaces.repositories.hashing import IHashingRepository
from app.auth.schemas import UserRegistrationCredentialsIn
from fastapi import HTTPException, status
from core.entities import UserRoleType
from core.interfaces.repositories.user_verification import IUserVerificationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.use_case import IUseCase


class RegisterUserUseCase(IUseCase):
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
        credentials: UserRegistrationCredentialsIn,
        role: UserRoleType,
    ) -> int:
        hashed = self.hashing.hash_password(credentials.password)
        user = await self.repository.get_by_email(session, credentials.email)
        is_verified = await self.verification.exist(
            credentials.email, credentials.operation_id
        )

        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {credentials.email} already registered",
            )

        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="you need to pass verification in one of the ways",
            )

        user_id = await self.repository.create(
            session,
            credentials.email,
            credentials.first_name,
            credentials.patronymic,
            credentials.surname,
            role,
            hashed,
        )
        await session.commit()
        await self.verification.delete(credentials.email, credentials.operation_id)
        self.logger.info(f"User {credentials.email} registered with id {user_id}")
        return user_id
