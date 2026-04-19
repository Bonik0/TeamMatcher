from core.interfaces.repositories.project import IProjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import ProjectWithRolesAndCompetences
from fastapi import HTTPException, status
from core.interfaces.use_case import IUseCase


class FindProjectByIdUseCase(IUseCase):
    def __init__(self, repository: IProjectRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, id: int
    ) -> tuple[ProjectWithRolesAndCompetences, int]:
        project = await self.repository.get_by_id(session, id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
        user_forms_count = await self.repository.get_user_forms_count(
            session, [project.id]
        )
        return project, user_forms_count[0]
