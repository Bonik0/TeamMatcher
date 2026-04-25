from sqlalchemy import select
from sqlalchemy.orm import selectinload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from core.models.postgres import (
    TeamDB,
    ProjectRoleAssociationDB,
    TeamMemberDB,
    ProjectDB,
)
from core.interfaces.repositories.team import ITeamRepository
from typing import Any
from core.entities import (
    ProjectStatus,
    ProjectWithRolesAndTeams,
)


class TeamRepository(ITeamRepository):
    def _parse_teams(self, projects: list[ProjectDB]) -> list[ProjectWithRolesAndTeams]:
        return [
            ProjectWithRolesAndTeams.model_validate(project, from_attributes=True)
            for project in projects
        ]

    async def create_bulk(
        self, session: AsyncSession, teams_data: list[dict[str, Any]]
    ) -> None:

        if not teams_data:
            return None

        team_values = [
            {
                "name": team_data["name"],
                "project_id": team_data["project_id"],
            }
            for team_data in teams_data
        ]
        members_by_team = [team_data["members"] for team_data in teams_data]

        team_query = insert(TeamDB).values(team_values).returning(TeamDB)
        result = await session.execute(team_query)
        created_teams = list(result.scalars().all())

        all_members_data = [
            {
                "team_id": team.id,
                "user_id": member["user_id"],
                "project_role_id": member["project_role_id"],
                "role_score": member["role_score"],
                "competence_match": member["competence_match"],
            }
            for team, members in zip(created_teams, members_by_team)
            for member in members
        ]
        query = insert(TeamMemberDB).values(all_members_data)
        await session.execute(query)

    async def get_by_organizer_id(
        self, session: AsyncSession, organizer_id: int
    ) -> list[ProjectWithRolesAndTeams]:
        query = (
            select(ProjectDB)
            .where(ProjectDB.organizer_id == organizer_id)
            .where(ProjectDB.status == ProjectStatus.COMPLETED)
            .options(
                selectinload(ProjectDB.teams)
                .selectinload(TeamDB.members)
                .selectinload(TeamMemberDB.user),
                selectinload(ProjectDB.roles).selectinload(
                    ProjectRoleAssociationDB.role
                ),
            )
            .order_by(ProjectDB.start_time.desc())
        )
        result = await session.execute(query)
        return self._parse_teams(result.scalars().all())

    async def get_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> list[ProjectWithRolesAndTeams]:

        query = (
            select(ProjectDB)
            .join(ProjectDB.teams)
            .join(TeamDB.members)
            .where(TeamMemberDB.user_id == user_id)
            .options(
                contains_eager(ProjectDB.teams)
                .selectinload(TeamDB.members)
                .selectinload(TeamMemberDB.user),
                selectinload(ProjectDB.roles).selectinload(
                    ProjectRoleAssociationDB.role
                ),
            )
            .order_by(ProjectDB.start_time.desc())
        )
        result = await session.execute(query)
        return self._parse_teams(result.scalars().unique().all())
