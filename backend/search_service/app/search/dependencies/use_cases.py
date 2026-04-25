from fastapi import Depends
from core.dependencies.repositories.role import get_role_repository
from core.dependencies.repositories.competence import get_competence_repository
from core.interfaces.repositories.role import IRoleRepository
from core.interfaces.repositories.competence import ICompetenceRepository
from app.search.use_cases.find_roles_use_case import FindRolesUseCase
from app.search.use_cases.find_competence_use_case import FindCompetenceUseCase
from app.search.use_cases.find_project_use_case import FindProjectUseCase
from core.interfaces.repositories.project import IProjectRepository
from core.dependencies.repositories.project import get_project_repository
from app.search.use_cases.find_project_by_id_use_case import FindProjectByIdUseCase


def get_find_role_use_case(
    repository: IRoleRepository = Depends(get_role_repository),
) -> FindRolesUseCase:
    return FindRolesUseCase(repository)


def get_find_competence_use_case(
    repository: ICompetenceRepository = Depends(get_competence_repository),
) -> FindCompetenceUseCase:
    return FindCompetenceUseCase(repository)


def get_find_project_use_case(
    repository: IProjectRepository = Depends(get_project_repository),
) -> FindProjectUseCase:
    return FindProjectUseCase(repository)


def get_find_project_by_id_use_case(
    repository: IProjectRepository = Depends(get_project_repository),
) -> FindProjectByIdUseCase:
    return FindProjectByIdUseCase(repository)
