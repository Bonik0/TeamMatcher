from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import ProjectWithRolesAndForms
from core.interfaces.use_case import IUseCase
from core.interfaces.repositories.project import IProjectRepository


class FindAllUserRoleUseCase(IUseCase):
    def __init__(self, repository: IProjectRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, user_id: int
    ) -> tuple[list[ProjectWithRolesAndForms], list[int]]:
        projects = await self.repository.get_user_projects_with_roles(session, user_id)
        user_forms_counts = await self.repository.get_user_forms_count(
            session, [project.id for project in projects]
        )
        return projects, user_forms_counts
