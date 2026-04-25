from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.competence import ICompetenceRepository
from app.user_competence.schemas import AddOrUpdateUserCompetenceIn
from fastapi import HTTPException, status
from core.interfaces.use_case import IUseCase


class AddOrUpdateUserCompetencesUseCase(IUseCase):
    def __init__(
        self,
        repository: ICompetenceRepository,
    ) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, user_id: int, form: AddOrUpdateUserCompetenceIn
    ) -> None:
        requested_ids = [competence.competence_id for competence in form.competences]
        existing_ids = await self.repository.get_existing_ids(session, requested_ids)
        missing_ids = set(requested_ids) - set(existing_ids)

        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Competence(s) with id(s) {sorted(missing_ids)} do not exist",
            )
        unique_competences = {}
        for user_competence in form.competences:
            unique_competences[user_competence.competence_id] = user_competence.level

        competences_data = [
            {"competence_id": competence_id, "level": level}
            for competence_id, level in unique_competences.items()
        ]
        await self.repository.add_or_update_user_competence_bulk(
            session, user_id, competences_data
        )
        await session.commit()
