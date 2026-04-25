from fastapi import Depends
from core.interfaces.repositories.project import IProjectRepository
from core.interfaces.repositories.role import IRoleRepository
from core.dependencies.repositories.project import get_project_repository
from core.dependencies.repositories.role import get_role_repository
from app.user_role.use_cases.add_or_update_user_role_use_case import (
    AddOrUpdateUserProjectApplicationUseCase,
)
from app.user_role.use_cases.delete_user_role_use_case import (
    DeleteUserProjectApplicationUseCase,
)
from app.user_role.use_cases.find_user_role_by_id_use_case import (
    FindUserRoleByProjectIdUseCase,
)
from app.user_role.use_cases.find_all_user_roles_use_case import FindAllUserRoleUseCase


def get_add_or_update_user_role_use_case(
    role_repository: IRoleRepository = Depends(get_role_repository),
    project_repository: IProjectRepository = Depends(get_project_repository),
) -> AddOrUpdateUserProjectApplicationUseCase:
    return AddOrUpdateUserProjectApplicationUseCase(
        role_repository=role_repository, project_repository=project_repository
    )


def get_delete_user_role_use_case(
    role_repository: IRoleRepository = Depends(get_role_repository),
    project_repository: IProjectRepository = Depends(get_project_repository),
) -> DeleteUserProjectApplicationUseCase:
    return DeleteUserProjectApplicationUseCase(
        role_repository=role_repository, project_repository=project_repository
    )


def get_find_user_role_by_user_id(
    role_repository: IRoleRepository = Depends(get_role_repository),
) -> FindUserRoleByProjectIdUseCase:
    return FindUserRoleByProjectIdUseCase(role_repository)


def get_find_all_use_roles_use_case(
    project_repository: IProjectRepository = Depends(get_project_repository),
) -> FindAllUserRoleUseCase:
    return FindAllUserRoleUseCase(project_repository)
