from core.interfaces.repositories.competence import ICompetenceRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import Competence
from core.interfaces.use_case import IUseCase


class FindCompetenceUseCase(IUseCase):
    def __init__(self, repository: ICompetenceRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, name_query: str | None, limit: int, offset: int
    ) -> list[Competence]:
        if not name_query:
            return await self.repository.get(session, limit, offset)
        return await self.repository.find_by_name(session, name_query, limit, offset)
