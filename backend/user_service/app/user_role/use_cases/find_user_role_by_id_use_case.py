from sqlalchemy.ext.asyncio import AsyncSession
from core.entities import UserProjectRole
from core.interfaces.use_case import IUseCase
from core.interfaces.repositories.role import IRoleRepository


class FindUserRoleByProjectIdUseCase(IUseCase):
    def __init__(self, repository: IRoleRepository) -> None:
        self.repository = repository

    async def execute(
        self, session: AsyncSession, user_id: int, project_id: int
    ) -> list[UserProjectRole]:
        return await self.repository.get_user_roles_by_user_and_project(
            session, user_id, project_id
        )
