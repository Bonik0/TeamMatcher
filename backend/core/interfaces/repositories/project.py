from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from core.entities import (
    Project,
    ProjectWithRolesAndCompetences,
    ProjectStatus,
    ProjectRole,
    ProjectRoleCompetence,
    ProjectWithRolesAndForms,
)


class IProjectRepository(Protocol):
    async def create(
        self,
        session: AsyncSession,
        organizer_id: int,
        name: str,
        description: str | None,
        start_time: datetime,
    ) -> Project:
        pass

    async def update(
        self,
        session: AsyncSession,
        project_id: int,
        name: str,
        description: str | None,
        start_time: datetime,
    ) -> None:
        pass

    async def update_status(
        self, session: AsyncSession, project_id: int, status: ProjectStatus
    ) -> None:
        pass

    async def get_by_id(
        self, session: AsyncSession, project_id: int
    ) -> ProjectWithRolesAndCompetences | None:
        pass

    async def get_by_organizer_id(
        self, session: AsyncSession, organizer_id: int
    ) -> list[ProjectWithRolesAndCompetences]:
        pass

    async def get_by_roles_and_competences(
        self,
        session: AsyncSession,
        search_vector_value: str | None,
        role_ids: list[int] | None,
        competence_ids: list[int] | None,
        limit: int,
        offset: int,
    ) -> list[ProjectWithRolesAndCompetences]:
        pass

    async def get_user_projects_with_roles(
        self, session: AsyncSession, user_id: int
    ) -> list[ProjectWithRolesAndForms]:
        pass

    async def create_or_update_role_associations(
        self,
        session: AsyncSession,
        project_id: int,
        project_roles: list[dict[str, int | str | None]],
    ) -> dict[int, ProjectRole]:
        pass

    async def create_or_update_role_competence_associations(
        self, session: AsyncSession, role_competencies: list[dict[str, int | float]]
    ) -> list[ProjectRoleCompetence]:
        pass
    
    async def delete_role_competence_associations(
        self, session: AsyncSession, project_role_ids: list[int]
    ) -> None:
        pass


    async def get_user_forms_count(
        self, session: AsyncSession, project_ids: list[int]
    ) -> list[int]:
        pass
