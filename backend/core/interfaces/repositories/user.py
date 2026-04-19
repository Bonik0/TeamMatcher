from typing import Protocol
from pydantic import EmailStr
from core.entities import User, UserRoleType, UserWithFormsAndCompetences
from sqlalchemy.ext.asyncio import AsyncSession


class IUserRepository(Protocol):
    async def create(
        self,
        session: AsyncSession,
        email: EmailStr,
        first_name: str,
        patronymic: str | None,
        surname: str,
        role: UserRoleType,
        hashed_password: str,
    ) -> int | None:
        pass

    async def get_by_email(self, session: AsyncSession, email: EmailStr) -> User | None:
        pass

    async def update_password(
        self, session: AsyncSession, email: EmailStr, new_hashed_password: str
    ) -> int | None:
        pass

    async def get_with_priorities_and_competences(
        self, session: AsyncSession, project_id: int
    ) -> list[UserWithFormsAndCompetences]:
        pass