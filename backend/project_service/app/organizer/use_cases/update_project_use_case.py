from sqlalchemy.ext.asyncio import AsyncSession
from app.organizer.use_cases.base_use_case import BaseProjectUseCase
from core.entities import ProjectStatus
from app.organizer.schemas import ProjectUpdateIn
from fastapi import HTTPException, status


class UpdateProjectUseCase(BaseProjectUseCase):
    async def execute(
        self, session: AsyncSession, organizer_id: int, form: ProjectUpdateIn
    ) -> None:
        project = await self.project.get_by_id(session, form.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {form.project_id} not found",
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
        new_role_names = set([role.name for role in form.roles])
        old_role_names = set([project_role.role.name for project_role in project.roles])
        if len(old_role_names & new_role_names) != len(old_role_names):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old roles cannot be deleted",
            )
        await self.project.update(
            session, project.id, form.name, form.description, form.start_time
        )
        await self._create_or_update_roles(session, project.id, form.roles)
        await self.utils.update(form.project_id, form.start_time.replace(tzinfo=None))
        await session.commit()
