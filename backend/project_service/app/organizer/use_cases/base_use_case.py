from sqlalchemy.ext.asyncio import AsyncSession
from app.organizer.schemas import RoleIn
from core.interfaces.repositories.project import IProjectRepository
from core.interfaces.repositories.role import IRoleRepository
from core.interfaces.repositories.competence import ICompetenceRepository
from core.interfaces.use_case import IUseCase
from app.organizer.utils import PlanFormatTeamsUtils


class BaseProjectUseCase(IUseCase):
    def __init__(
        self,
        project: IProjectRepository,
        role: IRoleRepository,
        competence: ICompetenceRepository,
        utils: PlanFormatTeamsUtils,
    ) -> None:
        self.project = project
        self.role = role
        self.competence = competence
        self.utils = utils

    async def _create_or_update_roles(
        self, session: AsyncSession, project_id: int, roles: list[RoleIn]
    ) -> int:
        role_names = list({role.name for role in roles})
        competence_names = list(
            {competence.name for role in roles for competence in role.competences}
        )

        roles_map = await self.role.get_or_create_bulk(session, role_names)
        competence_map = await self.competence.get_or_create_bulk(
            session, competence_names
        )

        project_roles = [
            {
                "role_id": roles_map[role.name].id,
                "description": role.description,
                "quantity_per_team": role.quantity_per_team,
            }
            for role in roles
        ]

        project_roles_map = await self.project.create_or_update_role_associations(
            session=session,
            project_id=project_id,
            project_roles=project_roles,
        )

        await self.project.delete_role_competence_associations(
            session, [project_role.id for project_role in project_roles_map.values()]
        )

        role_competencies = [
            {
                "project_role_id": project_roles_map[roles_map[role.name].id].id,
                "competence_id": competence_map[competence.name].id,
                "importance": competence.importance,
            }
            for role in roles
            for competence in role.competences
        ]

        await self.project.create_or_update_role_competence_associations(
            session=session, role_competencies=role_competencies
        )
