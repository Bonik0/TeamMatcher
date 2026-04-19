from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from pydantic import EmailStr
from core.interfaces.repositories.user import IUserRepository
from core.entities import User, UserRoleType, UserWithFormsAndCompetences
from core.models.postgres import UserDB, UserProjectRoleAssociationDB, ProjectRoleAssociationDB, UserCompetenceAssociationDB
from sqlalchemy.orm import contains_eager, selectinload


class SQLAlchemyUserRepository(IUserRepository):
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
        result = await session.execute(
            insert(UserDB)
            .values(
                email=email,
                first_name=first_name,
                patronymic=patronymic,
                surname=surname,
                role=role,
                hash_password=hashed_password,
            )
            .returning(UserDB.id)
        )
        return result.scalar_one()

    async def get_by_email(self, session: AsyncSession, email: EmailStr) -> User | None:
        result = await session.execute(select(UserDB).where(UserDB.email == email))
        user_db = result.scalar_one_or_none()
        if not user_db:
            return None
        return User.model_validate(user_db, from_attributes=True)

    async def update_password(
        self, session: AsyncSession, email: EmailStr, new_hashed_password: str
    ) -> int | None:
        result = await session.execute(
            update(UserDB)
            .where(UserDB.email == email)
            .values(hash_password=new_hashed_password)
            .returning(UserDB.id)
        )
        return result.scalar_one_or_none()


    async def get_with_priorities_and_competences(
        self, session: AsyncSession, project_id: int
    ) -> list[UserWithFormsAndCompetences]:
        
        query = (
            select(UserDB)
            .join(UserProjectRoleAssociationDB, UserDB.id == UserProjectRoleAssociationDB.user_id)
            .join(ProjectRoleAssociationDB, UserProjectRoleAssociationDB.project_role_id == ProjectRoleAssociationDB.id)
            .where(ProjectRoleAssociationDB.project_id == project_id)
            .options(
                contains_eager(UserDB.forms),
                selectinload(UserDB.competences)
            )
            .distinct()
        )
        result = await session.execute(query)
        return [
            UserWithFormsAndCompetences.model_validate(user, from_attributes=True)
            for user in result.unique().scalars().all()
        ]