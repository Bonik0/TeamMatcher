from fastapi import APIRouter, Depends, Path, Request
from core.dependencies.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import DeleteUserActionOut, UpdateUserActionOut
from core.dependencies.jwttoken import get_verifier
from core.entities import UserRoleType
from app.user_role.schemas import (
    AddOrUpdateUserRoleIn,
    DeleteUserProjectRolesIn,
    FindUserRoleByIdOut,
    UserRoleOut,
    ProjectOut,
    FindAllUserRolesOut,
)
from app.user_role.use_cases.add_or_update_user_role_use_case import (
    AddOrUpdateUserProjectApplicationUseCase,
)
from app.user_role.use_cases.delete_user_role_use_case import (
    DeleteUserProjectApplicationUseCase,
)
from app.user_role.dependencies.use_cases import (
    get_add_or_update_user_role_use_case,
    get_delete_user_role_use_case,
    get_find_user_role_by_user_id,
    get_find_all_use_roles_use_case,
)
from app.user_role.use_cases.find_user_role_by_id_use_case import (
    FindUserRoleByProjectIdUseCase,
)
from app.user_role.use_cases.find_all_user_roles_use_case import FindAllUserRoleUseCase


router = APIRouter(
    prefix="/role", tags=["Roles"], 
    dependencies=[get_verifier(UserRoleType.user)]
)


@router.get("/project/{project_id}")
async def find_user_roles_by_project_id(
    request: Request,
    project_id: int = Path(),
    use_case: FindUserRoleByProjectIdUseCase = Depends(get_find_user_role_by_user_id),
    session: AsyncSession = Depends(get_session),
) -> FindUserRoleByIdOut:
    roles = await use_case.execute(session, request.state.user_id, project_id)
    return FindUserRoleByIdOut(
        roles=[UserRoleOut.model_validate(role, from_attributes=True) for role in roles]
    )


@router.get("")
async def find_all_user_roles(
    request: Request,
    use_case: FindAllUserRoleUseCase = Depends(get_find_all_use_roles_use_case),
    session: AsyncSession = Depends(get_session),
) -> FindAllUserRolesOut:
    projects, user_forms_counts = await use_case.execute(session, request.state.user_id)
    return FindAllUserRolesOut(
        projects=[
            ProjectOut.model_validate(
                project.model_dump() | {"user_forms_count": user_forms_count}
            )
            for project, user_forms_count in zip(projects, user_forms_counts)
        ]
    )


@router.put("")
async def add_or_update_user_roles(
    request: Request,
    form: AddOrUpdateUserRoleIn,
    use_case: AddOrUpdateUserProjectApplicationUseCase = Depends(
        get_add_or_update_user_role_use_case
    ),
    session: AsyncSession = Depends(get_session),
) -> UpdateUserActionOut:
    await use_case.execute(session, request.state.user_id, form.project_id, form.roles)
    return UpdateUserActionOut()


@router.delete("")
async def delete_user_roles(
    request: Request,
    form: DeleteUserProjectRolesIn,
    use_case: DeleteUserProjectApplicationUseCase = Depends(
        get_delete_user_role_use_case
    ),
    session: AsyncSession = Depends(get_session),
) -> DeleteUserActionOut:
    await use_case.execute(session, request.state.user_id, form.project_id)
    return DeleteUserActionOut()
