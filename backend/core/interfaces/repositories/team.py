from typing import Protocol, Any
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import ProjectWithRolesAndTeams


class ITeamRepository(Protocol):
    async def create_bulk(
        self, session: AsyncSession, teams_data: list[dict[str, Any]]
    ) -> None:
        pass

    async def get_by_organizer_id(
        self, session: AsyncSession, organizer_id: int
    ) -> list[ProjectWithRolesAndTeams]:
        pass

    async def get_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> list[ProjectWithRolesAndTeams]:
        pass
