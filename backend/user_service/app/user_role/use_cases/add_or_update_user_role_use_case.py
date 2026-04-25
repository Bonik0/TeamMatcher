from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.project import IProjectRepository
from core.interfaces.repositories.role import IRoleRepository
from core.entities import ProjectStatus
from fastapi import HTTPException, status
from app.user_role.schemas import UserRoleIn
from core.interfaces.use_case import IUseCase


class AddOrUpdateUserProjectApplicationUseCase(IUseCase):
    def __init__(
        self,
        role_repository: IRoleRepository,
        project_repository: IProjectRepository,
    ) -> None:
        self.role_repository = role_repository
        self.project_repository = project_repository

    async def execute(
        self,
        session: AsyncSession,
        user_id: int,
        project_id: int,
        user_roles: list[UserRoleIn],
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
        user_role_ids = set([user_role.project_role_id for user_role in user_roles])
        valid_project_role_ids = set([role.id for role in project.roles])

        user_role_priorities = sorted([user_role.priority for user_role in user_roles])
        expected_priorities = list(range(1, len(user_roles) + 1))

        if user_role_priorities != expected_priorities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Priorities must be 1..{len(user_roles)} without gaps",
            )

        if len(user_role_ids) < len(user_roles):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate project_role_id in roles list",
            )

        if len(user_role_ids & valid_project_role_ids) < len(user_roles):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some project_role_ids are invalid or do not belong to the project",
            )

        roles_data = [
            {
                "project_role_id": user_role.project_role_id,
                "priority": user_role.priority,
            }
            for user_role in user_roles
        ]
        await self.role_repository.delete_user_roles_for_user_and_project(
            session, user_id, project_id
        )
        await self.role_repository.create_user_roles_bulk(session, user_id, roles_data)
        await session.commit()
