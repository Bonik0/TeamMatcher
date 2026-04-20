from fastapi import APIRouter, Depends, Path, Query
from app.search.schemas import (
    FindRoleIn,
    FindRoleOut,
    FindCompetenceIn,
    FindCompetenceOut,
    FindProjectIn,
    FindProjectOut,
    ProjectOut,
)
from app.search.use_cases.find_roles_use_case import FindRolesUseCase
from app.search.use_cases.find_competence_use_case import FindCompetenceUseCase
from app.search.dependencies.use_cases import (
    get_find_role_use_case,
    get_find_competence_use_case,
    get_find_project_use_case,
    get_find_project_by_id_use_case,
)
from core.dependencies.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.search.use_cases.find_project_use_case import FindProjectUseCase
from pydantic import NonNegativeInt
from app.search.use_cases.find_project_by_id_use_case import FindProjectByIdUseCase


router = APIRouter(
    tags=["Search"],
)


@router.get("/role")
async def find_role(
    form: FindRoleIn = Query(),
    use_case: FindRolesUseCase = Depends(get_find_role_use_case),
    session: AsyncSession = Depends(get_session),
) -> FindRoleOut:
    roles = await use_case.execute(session, form.q, form.limit, form.offset)
    return FindRoleOut(roles=roles)


@router.get("/competence")
async def find_competence(
    form: FindCompetenceIn = Query(),
    use_case: FindCompetenceUseCase = Depends(get_find_competence_use_case),
    session: AsyncSession = Depends(get_session),
) -> FindCompetenceOut:
    competencies = await use_case.execute(session, form.q, form.limit, form.offset)
    return FindCompetenceOut(competencies=competencies)


@router.get("/project")
async def find_project(
    form: FindProjectIn = Query(),
    use_case: FindProjectUseCase = Depends(get_find_project_use_case),
    session: AsyncSession = Depends(get_session),
) -> FindProjectOut:
    projects, user_forms_counts = await use_case.execute(
        session, form.q, form.role_ids, form.competence_ids, form.limit, form.offset
    )
    return FindProjectOut(
        projects=[
            ProjectOut.model_validate(
                project.model_dump() | {"user_forms_count": user_forms_count}
            )
            for project, user_forms_count in zip(projects, user_forms_counts)
        ]
    )


@router.get("/project/{id}")
async def find_project_by_id(
    id: NonNegativeInt = Path(),
    use_case: FindProjectByIdUseCase = Depends(get_find_project_by_id_use_case),
    session: AsyncSession = Depends(get_session),
) -> ProjectOut:
    project, forms_count = await use_case.execute(session, id)
    return ProjectOut.model_validate(
        project.model_dump() | {"user_forms_count": forms_count}
    )
