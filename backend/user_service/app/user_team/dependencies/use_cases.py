from core.dependencies.repositories.team import get_team_repository
from core.interfaces.repositories.team import ITeamRepository
from app.user_team.use_cases.find_user_teams_use_case import FindUserTeamsUseCase
from fastapi import Depends


def get_find_user_teams_use_case(
    repository: ITeamRepository = Depends(get_team_repository)
) -> FindUserTeamsUseCase:
    return FindUserTeamsUseCase(repository)