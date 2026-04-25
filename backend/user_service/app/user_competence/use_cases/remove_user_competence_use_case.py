from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.competence import ICompetenceRepository
from core.interfaces.use_case import IUseCase


class RemoveUserCompetencesUseCase(IUseCase):
    def __init__(
        self,
        repository: ICompetenceRepository,
    ) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, user_id: int, competence_ids: list[int]
    ) -> None:
        await self.repository.remove_user_competence_bulk(
            session, user_id, competence_ids
        )
        await session.commit()
