from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.project import IProjectRepository
from core.entities import ProjectWithRolesAndCompetences
from core.interfaces.use_case import IUseCase


class FindProjectUseCase(IUseCase):
    def __init__(self, repository: IProjectRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, organizer_id: int
    ) -> tuple[list[ProjectWithRolesAndCompetences], list[int]]:
        projects = await self.repository.get_by_organizer_id(session, organizer_id)
        user_forms_counts = await self.repository.get_user_forms_count(
            session, [project.id for project in projects]
        )
        return projects, user_forms_counts
