from fastapi import APIRouter, Depends, status, Request
from app.organizer.schemas import (
    ProjectCreateIn,
    ProjectCreateOut,
    ProjectFindOut,
    ProjectUpdateIn,
    ProjectCancelIn,
    ProjectOut,
    ProjectFormatingIn,
    FindProjectWithTeamsOut,
    FindOrganizerTeamsOut,
)
from app.organizer.use_cases.create_project_use_case import CreateProjectUseCase
from app.organizer.use_cases.find_project_use_case import FindProjectUseCase
from app.organizer.use_cases.start_teams_match_use_case import StartTeamsMatchUseCase
from app.organizer.dependencies.use_cases import (
    get_create_project_use_case,
    get_find_project_use_case,
    get_update_project_use_case,
    get_cancel_project_use_case,
    get_start_teams_match_use_case,
    get_find_teams_use_case,
)
from core.schemas import UpdateUserActionOut, DeleteUserActionOut
from app.organizer.use_cases.update_project_use_case import UpdateProjectUseCase
from app.organizer.use_cases.cancel_project_use_case import CancelProjectUseCase
from core.dependencies.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies.jwttoken import get_verifier
from core.entities import UserRoleType
from app.organizer.use_cases.find_teams_use_case import FindTeamsUseCase


router = APIRouter(
    tags=["Project CRUD for organizer"],
    dependencies=[get_verifier(UserRoleType.organizer)],
)


@router.get(path="/")
async def find_all_projects(
    request: Request,
    use_case: FindProjectUseCase = Depends(get_find_project_use_case),
    session: AsyncSession = Depends(get_session),
) -> ProjectFindOut:
    projects, user_forms_counts = await use_case.execute(session, request.state.user_id)
    return ProjectFindOut(
        projects=[
            ProjectOut.model_validate(
                project.model_dump() | {"user_forms_count": user_forms_count}
            )
            for project, user_forms_count in zip(projects, user_forms_counts)
        ]
    )


@router.put(path="/", status_code=status.HTTP_201_CREATED)
async def create_project(
    request: Request,
    form: ProjectCreateIn,
    create_project_use_case: CreateProjectUseCase = Depends(
        get_create_project_use_case
    ),
    session: AsyncSession = Depends(get_session),
) -> ProjectCreateOut:
    project_id = await create_project_use_case.execute(
        session, request.state.user_id, form
    )
    return ProjectCreateOut(project_id=project_id)


@router.post(path="/")
async def update_project(
    request: Request,
    form: ProjectUpdateIn,
    use_case: UpdateProjectUseCase = Depends(get_update_project_use_case),
    session: AsyncSession = Depends(get_session),
) -> UpdateUserActionOut:
    await use_case.execute(session, request.state.user_id, form)
    return UpdateUserActionOut()


@router.delete(path="/")
async def cancel_project(
    request: Request,
    form: ProjectCancelIn,
    use_case: CancelProjectUseCase = Depends(get_cancel_project_use_case),
    session: AsyncSession = Depends(get_session),
) -> DeleteUserActionOut:
    await use_case.execute(session, request.state.user_id, form.project_id)
    return DeleteUserActionOut()


@router.post("/match")
async def formating_teams(
    request: Request,
    form: ProjectFormatingIn,
    use_case: StartTeamsMatchUseCase = Depends(get_start_teams_match_use_case),
    session: AsyncSession = Depends(get_session),
) -> UpdateUserActionOut:
    await use_case.execute(session, request.state.user_id, form.project_id)
    return UpdateUserActionOut()


@router.get("/teams")
async def get_project_teams(
    request: Request,
    use_case: FindTeamsUseCase = Depends(get_find_teams_use_case),
    session: AsyncSession = Depends(get_session),
) -> FindOrganizerTeamsOut:
    projects = await use_case.execute(session, request.state.user_id)
    return FindOrganizerTeamsOut(
        projects=[
            FindProjectWithTeamsOut.model_validate(project, from_attributes=True)
            for project in projects
        ]
    )
