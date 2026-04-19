from sqlalchemy.orm import selectinload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.postgres import (
    ProjectDB,
    ProjectRoleAssociationDB,
    ProjectRoleCompetenceAssociationDB,
    UserProjectRoleAssociationDB,
)
from datetime import datetime
from sqlalchemy import select, update, delete, func
from sqlalchemy.dialects.postgresql import insert
from core.interfaces.repositories.project import IProjectRepository
from typing import Sequence
from core.entities import (
    Project,
    ProjectWithRolesAndCompetences,
    ProjectStatus,
    ProjectRole,
    ProjectRoleCompetence,
    ProjectWithRolesAndForms,
)


class SQLAlchemyProjectRepository(IProjectRepository):
    def _parse_project(self, project: ProjectDB) -> Project:
        return Project.model_validate(project, from_attributes=True)

    def _parse_project_role(
        self, project_role: ProjectRoleAssociationDB
    ) -> ProjectRole:
        return ProjectRole.model_validate(project_role, from_attributes=True)

    def _parse_project_role_competence(
        self, project_role_competence: ProjectRoleCompetenceAssociationDB
    ) -> ProjectRoleCompetence:
        return ProjectRoleCompetence.model_validate(
            project_role_competence, from_attributes=True
        )

    def _parse_project_with_roles_and_competences(
        self, project: ProjectDB
    ) -> ProjectWithRolesAndCompetences:
        return ProjectWithRolesAndCompetences.model_validate(
            project, from_attributes=True
        )

    def _parse_projects_with_roles_and_competences(
        self, projects: Sequence[ProjectDB]
    ) -> list[ProjectWithRolesAndCompetences]:
        return [
            ProjectWithRolesAndCompetences.model_validate(project, from_attributes=True)
            for project in projects
        ]

    def _parse_project_with_roles_and_forms(
        self, projects: Sequence[ProjectDB]
    ) -> list[ProjectWithRolesAndForms]:
        return [
            ProjectWithRolesAndForms.model_validate(project, from_attributes=True)
            for project in projects
        ]

    async def create(
        self,
        session: AsyncSession,
        organizer_id: int,
        name: str,
        description: str | None,
        start_time: datetime,
    ) -> Project:
        query = (
            insert(ProjectDB)
            .values(
                name=name,
                status=ProjectStatus.RECRUITING,
                organizer_id=organizer_id,
                description=description,
                start_time=start_time.replace(tzinfo=None),
            )
            .returning(ProjectDB)
        )

        project = await session.execute(query)
        return self._parse_project(project.scalar_one())

    async def update(
        self,
        session: AsyncSession,
        project_id: int,
        name: str,
        description: str | None,
        start_time: datetime,
    ) -> None:
        query = (
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(
                name=name,
                description=description,
                start_time=start_time.replace(tzinfo=None),
            )
        )

        await session.execute(query)

    async def update_status(
        self, session: AsyncSession, project_id: int, status: ProjectStatus
    ) -> None:
        await session.execute(
            update(ProjectDB).where(ProjectDB.id == project_id).values(status=status)
        )

    async def get_by_id(
        self, session: AsyncSession, project_id: int
    ) -> ProjectWithRolesAndCompetences | None:
        result = await session.execute(
            select(ProjectDB)
            .where(ProjectDB.id == project_id)
            .options(
                selectinload(ProjectDB.roles).selectinload(
                    ProjectRoleAssociationDB.role
                ),
                selectinload(ProjectDB.roles)
                .selectinload(ProjectRoleAssociationDB.competences)
                .selectinload(ProjectRoleCompetenceAssociationDB.competence),
            )
        )
        project = result.scalar_one_or_none()
        if project is None:
            return
        return self._parse_project_with_roles_and_competences(project)

    async def get_by_organizer_id(
        self, session: AsyncSession, organizer_id: int
    ) -> list[ProjectWithRolesAndCompetences]:
        result = await session.execute(
            select(ProjectDB)
            .where(ProjectDB.organizer_id == organizer_id)
            .options(
                selectinload(ProjectDB.roles).selectinload(
                    ProjectRoleAssociationDB.role
                ),
                selectinload(ProjectDB.roles)
                .selectinload(ProjectRoleAssociationDB.competences)
                .selectinload(ProjectRoleCompetenceAssociationDB.competence),
            )
            .order_by(ProjectDB.id.desc())
        )

        return self._parse_projects_with_roles_and_competences(result.scalars().all())

    async def get_by_roles_and_competences(
        self,
        session: AsyncSession,
        search_vector_value: str | None,
        role_ids: list[int] | None,
        competence_ids: list[int] | None,
        limit: int,
        offset: int,
    ) -> list[ProjectWithRolesAndCompetences]:
        query = (
            select(ProjectDB)
            .where(ProjectDB.start_time > datetime.now().replace(tzinfo=None))
            .where(ProjectDB.status == ProjectStatus.RECRUITING)
        )
        if search_vector_value:
            query = query.where(
                ProjectDB.name.like(f"%{search_vector_value}%")
                | ProjectDB.description.like(f"%{search_vector_value}%")
            )

        if role_ids:
            query = query.where(
                ProjectDB.id.in_(
                    select(ProjectRoleAssociationDB.project_id).where(
                        ProjectRoleAssociationDB.role_id.in_(role_ids)
                    )
                )
            )

        if competence_ids:
            query = query.where(
                ProjectDB.id.in_(
                    select(ProjectRoleAssociationDB.project_id).where(
                        ProjectRoleAssociationDB.id.in_(
                            select(
                                ProjectRoleCompetenceAssociationDB.project_role_id
                            ).where(
                                ProjectRoleCompetenceAssociationDB.competence_id.in_(
                                    competence_ids
                                )
                            )
                        )
                    )
                )
            )

        query = (
            query.options(
                selectinload(ProjectDB.roles).selectinload(
                    ProjectRoleAssociationDB.role
                ),
                selectinload(ProjectDB.roles)
                .selectinload(ProjectRoleAssociationDB.competences)
                .selectinload(ProjectRoleCompetenceAssociationDB.competence),
            )
            .order_by(ProjectDB.start_time)
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(query)

        return self._parse_projects_with_roles_and_competences(result.scalars().all())

    async def get_user_projects_with_roles(
        self, session: AsyncSession, user_id: int
    ) -> list[ProjectWithRolesAndForms]:
        query = (
            select(ProjectDB)
            .join(ProjectDB.roles)
            .join(ProjectRoleAssociationDB.forms)
            .where(UserProjectRoleAssociationDB.user_id == user_id)
            .options(
                contains_eager(ProjectDB.roles).contains_eager(
                    ProjectRoleAssociationDB.forms
                ),
                contains_eager(ProjectDB.roles).contains_eager(
                    ProjectRoleAssociationDB.role
                ),
            )
        )
        result = await session.execute(query)
        return self._parse_project_with_roles_and_forms(result.scalars().unique().all())

    async def get_user_forms_count(
        self, session: AsyncSession, project_ids: list[int]
    ) -> list[int]:
        query = (
            select(
                ProjectRoleAssociationDB.project_id,
                func.count(func.distinct(UserProjectRoleAssociationDB.user_id)).label(
                    "count"
                ),
            )
            .join(
                UserProjectRoleAssociationDB,
                ProjectRoleAssociationDB.id
                == UserProjectRoleAssociationDB.project_role_id,
            )
            .where(ProjectRoleAssociationDB.project_id.in_(project_ids))
            .group_by(ProjectRoleAssociationDB.project_id)
        )
        result = await session.execute(query)
        counts = {project_id: count for project_id, count in result.all()}
        return [counts.get(project_id, 0) for project_id in project_ids]

    async def create_or_update_role_associations(
        self,
        session: AsyncSession,
        project_id: int,
        project_roles: list[dict[str, int | str | None]],
    ) -> dict[int, ProjectRole]:
        if not project_roles:
            return {}
        query = insert(ProjectRoleAssociationDB).values(
            [
                {
                    "project_id": project_id,
                    "role_id": project_role["role_id"],
                    "description": project_role["description"],
                    "quantity_per_team": project_role["quantity_per_team"],
                }
                for project_role in project_roles
            ]
        )

        query = query.on_conflict_do_update(
            index_elements=["project_id", "role_id"],
            set_={
                "description": query.excluded.description,
                "quantity_per_team": query.excluded.quantity_per_team,
            },
        ).returning(ProjectRoleAssociationDB)

        result = await session.execute(query)

        return {
            project_role.role_id: project_role
            for project_role in map(
                lambda project_role: self._parse_project_role(project_role),
                result.scalars().all(),
            )
        }

    async def create_or_update_role_competence_associations(
        self, session: AsyncSession, role_competencies: list[dict[str, int | float]]
    ) -> list[ProjectRoleCompetence]:
        if not role_competencies:
            return []
        query = insert(ProjectRoleCompetenceAssociationDB).values(
            [
                {
                    "project_role_id": competence["project_role_id"],
                    "competence_id": competence["competence_id"],
                    "importance": competence["importance"],
                }
                for competence in role_competencies
            ]
        )
        query = query.on_conflict_do_update(
            index_elements=["project_role_id", "competence_id"],
            set_={
                "importance": query.excluded.importance,
            },
        ).returning(ProjectRoleCompetenceAssociationDB)

        result = await session.execute(query)
        return [
            self._parse_project_role_competence(project_competence)
            for project_competence in result.scalars().all()
        ]

    async def delete_role_competence_associations(
        self, session: AsyncSession, project_role_ids: list[int]
    ) -> None:
        await session.execute(
            delete(ProjectRoleCompetenceAssociationDB).where(
                ProjectRoleCompetenceAssociationDB.project_role_id.in_(project_role_ids)
            )
        )
