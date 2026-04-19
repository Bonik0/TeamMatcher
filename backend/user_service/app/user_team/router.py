from fastapi import APIRouter, Depends, Request
from core.dependencies.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.jwttoken import get_verifier
from core.entities import UserRoleType
from app.user_team.dependencies.use_cases import get_find_user_teams_use_case
from app.user_team.use_cases.find_user_teams_use_case import FindUserTeamsUseCase
from app.user_team.schemas import FindUserTeamsOut, FindTeamOut

router = APIRouter(
    prefix="/team", tags=["Teams"], dependencies=[get_verifier(UserRoleType.user)]
)


@router.get("")
async def get_user_teams(
    request: Request,
    use_case: FindUserTeamsUseCase = Depends(get_find_user_teams_use_case),
    session: AsyncSession = Depends(get_session),
) -> FindUserTeamsOut:
    teams = await use_case.execute(session, request.state.user_id)
    return FindUserTeamsOut(
        teams=[FindTeamOut.model_validate(team, from_attributes=True) for team in teams]
    )
