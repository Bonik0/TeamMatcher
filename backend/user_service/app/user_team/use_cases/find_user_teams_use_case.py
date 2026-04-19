from core.interfaces.use_case import IUseCase
from core.interfaces.repositories.team import ITeamRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import TeamWithMembersAndProject



class FindUserTeamsUseCase(IUseCase):
    
    def __init__(self, repository: ITeamRepository) -> None:
        self.repository = repository
        
        
    async def execute(self, session: AsyncSession, user_id: int) -> list[TeamWithMembersAndProject]:
        return await self.repository.get_by_user_id(session, user_id)