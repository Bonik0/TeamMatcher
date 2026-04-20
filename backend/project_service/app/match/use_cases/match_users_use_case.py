from core.interfaces.use_case import IUseCase
from sqlalchemy.ext.asyncio import AsyncSession
from core.interfaces.repositories.project import IProjectRepository
from core.interfaces.repositories.user import IUserRepository
from core.entities import ProjectStatus
from app.match.utils.interfaces import IMatchUtils
from core.interfaces.repositories.team import ITeamRepository
from logging import Logger


class MatchUsersUseCase(IUseCase):
    def __init__(
        self,
        project_repository: IProjectRepository,
        user_repository: IUserRepository,
        team_repository: ITeamRepository,
        match_utils: IMatchUtils,
        logger: Logger,
    ) -> None:
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.team_repository = team_repository
        self.match_utils = match_utils
        self.logger = logger

    async def _change_project_status(
        self, session: AsyncSession, project_id: int, status: ProjectStatus
    ) -> None:
        await self.project_repository.update_status(session, project_id, status)

    async def execute(self, session: AsyncSession, project_id: int) -> None:
        project = await self.project_repository.get_by_id(session, project_id)
        users = await self.user_repository.get_with_priorities_and_competences(
            session, project_id
        )

        if not project:
            self.logger.info(f"incorrect project_id: {project_id}")
            return

        if not users:
            self.logger.info("No users data")
            await self._change_project_status(
                session, project_id, ProjectStatus.COMPLETED
            )
            await session.commit()
            return

        self.logger.info(f"{project=}")
        self.logger.info("Users for format by project:\n")
        self.logger.info("\n".join([user.model_dump_json(indent=1) for user in users]))

        await self._change_project_status(session, project_id, ProjectStatus.FORMATED)
        await session.commit()

        teams = self.match_utils.execute(users, project.roles)

        self.logger.info(f"Balanced teams for {project_id=}\n")
        self.logger.info(
            "\n".join(
                f"{team_index}:{user_index}. {user}"
                for team_index, team in enumerate(teams)
                for user_index, user in enumerate(team)
            )
        )

        await self._change_project_status(session, project_id, ProjectStatus.COMPLETED)
        await self.team_repository.create_bulk(
            session,
            [
                {
                    "name": f"Команда № {team_index}",
                    "project_id": project_id,
                    "members": [
                        {
                            "user_id": user.user_id,
                            "project_role_id": user.project_role_id,
                            "role_score": user.role_score,
                            "competence_match": user.competence_match,
                        }
                        for user in team
                    ],
                }
                for team_index, team in enumerate(teams, start=1)
            ],
        )
        await session.commit()
