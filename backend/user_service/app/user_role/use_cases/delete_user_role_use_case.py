from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.use_case import IUseCase
from core.interfaces.repositories.role import IRoleRepository
from core.interfaces.repositories.project import IProjectRepository
from fastapi import HTTPException, status
from core.entities import ProjectStatus


class DeleteUserProjectApplicationUseCase(IUseCase):
    def __init__(
        self, role_repository: IRoleRepository, project_repository: IProjectRepository
    ) -> None:
        self.role_repository = role_repository
        self.project_repository = project_repository

    async def execute(
        self, session: AsyncSession, user_id: int, project_id: int
    ) -> None:
        project = await self.project_repository.get_by_id(session, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found",
            )
        if project.status != ProjectStatus.RECRUITING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can apply only to RECRUITING projects",
            )
        await self.role_repository.delete_user_roles_for_user_and_project(
            session, user_id, project_id
        )
        await session.commit()
