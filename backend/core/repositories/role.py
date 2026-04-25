from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.postgres import (
    RoleDB,
    UserProjectRoleAssociationDB,
    ProjectRoleAssociationDB,
)
from core.entities import Role, UserProjectRole
from sqlalchemy.dialects.postgresql import insert
from core.interfaces.repositories.role import IRoleRepository
from typing import Sequence


class SQLAlchemyRoleRepository(IRoleRepository):
    def _parse_roles(self, roles: Sequence[RoleDB]) -> list[Role]:
        return [Role.model_validate(role, from_attributes=True) for role in roles]

    async def get_by_names(self, session: AsyncSession, names: list[str]) -> list[Role]:
        if not names:
            return []
        result = await session.execute(select(RoleDB).where(RoleDB.name.in_(names)))
        return self._parse_roles(result.scalars().all())

    async def get(self, session: AsyncSession, limit: int, offset: int) -> list[Role]:
        query = select(RoleDB).order_by(RoleDB.name).limit(limit).offset(offset)
        result = await session.execute(query)
        return self._parse_roles(result.scalars().all())

    async def find_by_name(
        self, session: AsyncSession, name_query: str, limit: int, offset: int
    ) -> list[Role]:
        query = (
            select(RoleDB)
            .where(RoleDB.name.like(f"%{name_query}%"))
            .order_by(RoleDB.name)
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)
        return self._parse_roles(result.scalars().all())

    async def create_bulk(self, session: AsyncSession, names: list[str]) -> list[Role]:
        query = (
            insert(RoleDB)
            .on_conflict_do_nothing(index_elements=["id"])
            .returning(RoleDB)
            .values([{"name": name} for name in set(names)])
        )
        result = await session.execute(query)
        return self._parse_roles(result.scalars().all())

    async def get_or_create_bulk(
        self, session: AsyncSession, names: list[str]
    ) -> dict[str, Role]:
        if not names:
            return {}

        names = list(set(names))

        existing_roles = await self.get_by_names(session, names)

        existing_names = [role.name for role in existing_roles]
        missing_names = [name for name in names if name not in existing_names]

        if missing_names:
            new_roles = await self.create_bulk(session, list(missing_names))
            existing_roles.extend(new_roles)

        return {role.name: role for role in existing_roles}

    async def create_user_roles_bulk(
        self, session: AsyncSession, user_id: int, form: list[dict[str, int]]
    ) -> None:
        if not form:
            return None

        query = insert(UserProjectRoleAssociationDB).values(
            [
                {
                    "user_id": user_id,
                    "project_role_id": role["project_role_id"],
                    "priority": role["priority"],
                }
                for role in form
            ]
        )
        await session.execute(query)

    async def delete_user_roles_for_user_and_project(
        self, session: AsyncSession, user_id: int, project_id: int
    ) -> None:
        query = delete(UserProjectRoleAssociationDB).where(
            UserProjectRoleAssociationDB.user_id == user_id,
            UserProjectRoleAssociationDB.project_role_id.in_(
                select(ProjectRoleAssociationDB)
                .where(ProjectRoleAssociationDB.project_id == project_id)
                .with_only_columns(ProjectRoleAssociationDB.id)
            ),
        )
        await session.execute(query)

    async def get_user_roles_by_user_and_project(
        self, session: AsyncSession, user_id: int, project_id: int
    ) -> list[UserProjectRole]:
        query = (
            select(UserProjectRoleAssociationDB)
            .join(
                ProjectRoleAssociationDB,
                ProjectRoleAssociationDB.id
                == UserProjectRoleAssociationDB.project_role_id,
            )
            .where(
                UserProjectRoleAssociationDB.user_id == user_id,
                ProjectRoleAssociationDB.project_id == project_id,
            )
            .order_by(UserProjectRoleAssociationDB.priority)
        )
        result = await session.execute(query)
        return [
            UserProjectRole.model_validate(user_project_role, from_attributes=True)
            for user_project_role in result.scalars().all()
        ]
