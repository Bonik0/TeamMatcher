from core.interfaces.use_case import IUseCase
from core.interfaces.repositories.team import ITeamRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import TeamWithMembersAndProject


class FindTeamsUseCase(IUseCase):
    def __init__(self, repository: ITeamRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, organizer_id: int
    ) -> list[TeamWithMembersAndProject]:
        return await self.repository.get_by_organizer_id(session, organizer_id)
