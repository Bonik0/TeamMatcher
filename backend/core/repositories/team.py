from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from core.models.postgres import TeamDB, ProjectRoleAssociationDB, TeamMemberDB, ProjectDB
from core.interfaces.repositories.team import ITeamRepository
from typing import Any
import logging
from core.entities import TeamWithMembersAndProject, ProjectStatus, ProjectWithRolesAndTeams

class TeamRepository(ITeamRepository):
    
    
    def _parse_teams(self, teams: list[TeamDB]) -> list[TeamWithMembersAndProject]:
        return [
            TeamWithMembersAndProject.model_validate(team, from_attributes=True)
            for team in teams
        ]

    async def create_bulk(
        self,
        session: AsyncSession,
        teams_data: list[dict[str, Any]]
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
        members_by_team = [
            team_data["members"]
            for team_data in teams_data
        ] 

        team_query = insert(TeamDB).values(team_values).returning(TeamDB)
        result = await session.execute(team_query)
        created_teams = list(result.scalars().all())

        all_members_data = [
            {
                "team_id": team.id,
                "user_id": member["user_id"],
                "project_role_id": member["project_role_id"],
                "role_score": member["role_score"],
                "competence_match": member["competence_match"]
            }
            for team, members in zip(created_teams, members_by_team)
            for member in members
        ]
        query = insert(TeamMemberDB).values(all_members_data)
        await session.execute(query)


    async def get_by_organizer_id(
        self,
        session: AsyncSession,
        organizer_id: int
    ) -> list[ProjectWithRolesAndTeams]:
        query = (
            select(ProjectDB)
            .where(ProjectDB.organizer_id == organizer_id)
            .where(ProjectDB.status == ProjectStatus.COMPLETED)
            .options(
                selectinload(ProjectDB.teams)
                .selectinload(TeamDB.members)
                .selectinload(TeamMemberDB.user),
                selectinload(ProjectDB.roles)
                .selectinload(ProjectRoleAssociationDB.role)
            )
        )
        result = await session.execute(query)
        return [
            ProjectWithRolesAndTeams.model_validate(project, from_attributes=True)
            for project in result.scalars().all()
        ] 

    async def get_by_user_id(
        self,
        session: AsyncSession,
        user_id: int
    ) -> list[TeamWithMembersAndProject]:

        query = (
            select(TeamDB)
            .where(
                TeamDB.id.in_(
                    select(
                        TeamMemberDB.team_id
                    ).where(
                        TeamMemberDB.user_id == user_id
                    ).subquery()
                )
            )
            .options(
                selectinload(TeamDB.members)
                .selectinload(TeamMemberDB.user),
                selectinload(TeamDB.project),
                selectinload(TeamDB.members)
                .selectinload(TeamMemberDB.project_role)
                .selectinload(ProjectRoleAssociationDB.role)
            )
        )
        result = await session.execute(query)
        return [
            TeamWithMembersAndProject.model_validate(team, from_attributes=True)
            for team in result.scalars().all()
        ]