from fastapi import APIRouter, Depends, Request
from core.dependencies.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.user_competence.schemas import (
    AddOrUpdateUserCompetenceIn,
    RemoveUserCompetenceIn,
    UserCompetenceOut,
    UserCompetencesOut,
)
from app.user_competence.use_cases.add_or_update_user_competence_use_case import (
    AddOrUpdateUserCompetencesUseCase,
)
from app.user_competence.use_cases.remove_user_competence_use_case import (
    RemoveUserCompetencesUseCase,
)
from app.user_competence.use_cases.find_user_competence_use_case import (
    FindUserCompetencesUseCase,
)
from app.user_competence.dependencies.use_cases import (
    get_add_or_update_use_case,
    get_find_use_case,
    get_remove_use_case,
)
from core.schemas import DeleteUserActionOut, UpdateUserActionOut
from core.dependencies.jwttoken import get_verifier
from core.entities import UserRoleType


router = APIRouter(
    prefix="/competence",
    tags=["Competences"],
    dependencies=[get_verifier(UserRoleType.user)],
)


@router.get("")
async def find_user_competence(
    request: Request,
    use_case: FindUserCompetencesUseCase = Depends(get_find_use_case),
    session: AsyncSession = Depends(get_session),
) -> UserCompetencesOut:
    user_competences = await use_case.execute(session, request.state.user_id)
    return UserCompetencesOut(
        competences=[
            UserCompetenceOut.model_validate(user_competence, from_attributes=True)
            for user_competence in user_competences
        ]
    )


@router.post("")
async def add_or_update_user_competence(
    request: Request,
    form: AddOrUpdateUserCompetenceIn,
    use_case: AddOrUpdateUserCompetencesUseCase = Depends(get_add_or_update_use_case),
    session: AsyncSession = Depends(get_session),
) -> None:
    await use_case.execute(session, request.state.user_id, form)
    return UpdateUserActionOut()


@router.delete("")
async def remove_user_competence(
    request: Request,
    form: RemoveUserCompetenceIn,
    use_case: RemoveUserCompetencesUseCase = Depends(get_remove_use_case),
    session: AsyncSession = Depends(get_session),
) -> DeleteUserActionOut:
    await use_case.execute(session, request.state.user_id, form.competence_ids)
    return DeleteUserActionOut()
