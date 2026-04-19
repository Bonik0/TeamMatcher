from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.project import IProjectRepository
from core.entities import ProjectStatus
from fastapi import HTTPException, status
from core.interfaces.use_case import IUseCase
from app.organizer.utils import PlanFormatTeamsUtils

class CancelProjectUseCase(IUseCase):
    def __init__(self, repository: IProjectRepository, utils: PlanFormatTeamsUtils) -> None:
        self.repository = repository
        self.utils = utils

    async def execute(
        self, session: AsyncSession, organizer_id: int, project_id: int
    ) -> None:
        project = await self.repository.get_by_id(session, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found",
            )
        if project.status != ProjectStatus.RECRUITING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project can be updated only in RECRUITING status",
            )
        if project.organizer_id != organizer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Is not your project"
            )
        await self.repository.update_status(
            session, project_id, ProjectStatus.CANCELLED
        )
        await self.utils.cancel(project.id)
        await session.commit()
