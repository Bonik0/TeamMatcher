from app.organizer.use_cases.create_project_use_case import CreateProjectUseCase
from core.dependencies.repositories.project import get_project_repository
from core.dependencies.repositories.role import get_role_repository
from core.dependencies.repositories.competence import get_competence_repository
from core.interfaces.repositories.project import IProjectRepository
from core.interfaces.repositories.role import IRoleRepository
from core.interfaces.repositories.competence import ICompetenceRepository
from app.organizer.use_cases.find_project_use_case import FindProjectUseCase
from app.organizer.use_cases.update_project_use_case import UpdateProjectUseCase
from app.organizer.use_cases.cancel_project_use_case import CancelProjectUseCase
from fastapi import Depends
from app.organizer.utils import PlanFormatTeamsUtils
from app.organizer.dependencies.utils import get_formating_teams_utils
from app.organizer.use_cases.start_teams_match_use_case import StartTeamsMatchUseCase
from core.dependencies.repositories.team import get_team_repository
from core.interfaces.repositories.team import ITeamRepository
from app.organizer.use_cases.find_teams_use_case import FindTeamsUseCase


def get_create_project_use_case(
    project: IProjectRepository = Depends(get_project_repository),
    role: IRoleRepository = Depends(get_role_repository),
    competence: ICompetenceRepository = Depends(get_competence_repository),
    utils: PlanFormatTeamsUtils = Depends(get_formating_teams_utils),
) -> CreateProjectUseCase:
    return CreateProjectUseCase(project, role, competence, utils)


def get_find_project_use_case(
    project: IProjectRepository = Depends(get_project_repository),
) -> FindProjectUseCase:
    return FindProjectUseCase(project)


def get_update_project_use_case(
    project: IProjectRepository = Depends(get_project_repository),
    role: IRoleRepository = Depends(get_role_repository),
    competence: ICompetenceRepository = Depends(get_competence_repository),
    utils: PlanFormatTeamsUtils = Depends(get_formating_teams_utils),
) -> UpdateProjectUseCase:
    return UpdateProjectUseCase(project, role, competence, utils)


def get_cancel_project_use_case(
    project: IProjectRepository = Depends(get_project_repository),
    utils: PlanFormatTeamsUtils = Depends(get_formating_teams_utils),
) -> CancelProjectUseCase:
    return CancelProjectUseCase(project, utils)


def get_start_teams_match_use_case(
    project: IProjectRepository = Depends(get_project_repository),
    utils: PlanFormatTeamsUtils = Depends(get_formating_teams_utils),
) -> StartTeamsMatchUseCase:
    return StartTeamsMatchUseCase(project, utils)


def get_find_teams_use_case(
    repository: ITeamRepository = Depends(get_team_repository),
) -> FindTeamsUseCase:
    return FindTeamsUseCase(repository)
