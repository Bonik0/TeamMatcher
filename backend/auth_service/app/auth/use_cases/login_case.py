from core.interfaces.repositories.user import IUserRepository
from core.interfaces.repositories.hashing import IHashingRepository
from app.auth.schemas import UserLoginCredentialsIn
from fastapi import HTTPException, status
from core.entities import User
from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.use_case import IUseCase


class LoginUserUseCase(IUseCase):
    def __init__(
        self, repository: IUserRepository, hashing: IHashingRepository
    ) -> None:
        self.repository = repository
        self.hashing = hashing

    async def execute(
        self, session: AsyncSession, credentials: UserLoginCredentialsIn
    ) -> User:
        user = await self.repository.get_by_email(session, credentials.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {credentials.email} not found",
            )
        if not self.hashing.verify_password(credentials.password, user.hash_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
            )
        return user
