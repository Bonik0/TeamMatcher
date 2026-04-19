from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.competence import ICompetenceRepository
from core.entities import UserCompetenceWithCompetence
from core.interfaces.use_case import IUseCase


class FindUserCompetencesUseCase(IUseCase):
    def __init__(
        self,
        repository: ICompetenceRepository,
    ) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, user_id: int
    ) -> list[UserCompetenceWithCompetence]:
        return await self.repository.get_user_competences_by_user_id(session, user_id)
