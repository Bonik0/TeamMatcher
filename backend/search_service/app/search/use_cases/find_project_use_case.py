from core.interfaces.repositories.project import IProjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import ProjectWithRolesAndCompetences
from core.interfaces.use_case import IUseCase


class FindProjectUseCase(IUseCase):
    def __init__(self, repository: IProjectRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        session: AsyncSession,
        search_vector_value: str | None,
        role_ids: list[int] | None,
        competence_ids: list[int] | None,
        limit: int,
        offset: int,
    ) -> tuple[list[ProjectWithRolesAndCompetences], list[int]]:
        projects = await self.repository.get_by_roles_and_competences(
            session, search_vector_value, role_ids, competence_ids, limit, offset
        )
        user_forms_counts = await self.repository.get_user_forms_count(
            session, [project.id for project in projects]
        )
        return projects, user_forms_counts
