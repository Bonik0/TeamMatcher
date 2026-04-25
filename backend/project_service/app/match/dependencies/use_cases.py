from app.match.use_cases.match_users_use_case import MatchUsersUseCase
from core.interfaces.repositories.project import IProjectRepository
from core.interfaces.repositories.user import IUserRepository
from app.match.utils.interfaces import IMatchUtils
from core.interfaces.repositories.team import ITeamRepository
from logging import Logger


def get_match_use_case(
    project_repository: IProjectRepository,
    user_repository: IUserRepository,
    team_repository: ITeamRepository,
    match_utils: IMatchUtils,
    logger: Logger,
) -> MatchUsersUseCase:
    return MatchUsersUseCase(
        project_repository, user_repository, team_repository, match_utils, logger
    )
