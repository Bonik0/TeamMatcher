from fastapi import APIRouter, Depends
from core.jwttoken.schemas import AuthAPIHeaderIn
from app.jwttoken.dependencies.user_cases import (
    get_validate_token_use_case,
    get_update_tokens_use_case,
    get_logout_use_case,
    get_full_logout_use_case,
)
from app.jwttoken.user_cases.validate_token_use_case import ValidateTokenUseCase
from core.entities import JWTTokenPayload, JWTTokenType
from app.jwttoken.user_cases.update_token_use_case import UpdateTokensUseCase
from app.jwttoken.dependencies.utils import (
    get_jwt_token_generator,
    get_jwt_token_service,
    get_auth_header_verify,
)
from app.jwttoken.utils import JWTGenerator
from core.jwttoken.schemas import IssuedJWTTokensOut
from app.jwttoken.schemas import UpdateTokensIn
from app.jwttoken.user_cases.logout_use_case import LogoutUseCase
from core.schemas import UserActionOut
from app.jwttoken.user_cases.full_logout_use_case import FullLogoutUseCase
from app.jwttoken.utils import JWTService, AuthHeaderVerifyUtils


router = APIRouter(prefix="/token", tags=["Work with tokens"])


@router.get(
    path="",
    summary="Verify token",
)
async def verify_access_token(
    authorization_header: AuthAPIHeaderIn,
    header_verify: AuthHeaderVerifyUtils = Depends(get_auth_header_verify),
    validate_use_case: ValidateTokenUseCase = Depends(get_validate_token_use_case),
) -> JWTTokenPayload:
    token = header_verify.verify(authorization_header)
    return await validate_use_case.execute(token, JWTTokenType.ACCESS)


@router.post(
    path="/update",
    summary="Token update",
)
async def update_tokens(
    form: UpdateTokensIn,
    jwttoken_service: JWTService = Depends(get_jwt_token_service),
    update_tokens_use_case: UpdateTokensUseCase = Depends(get_update_tokens_use_case),
    token_generator: JWTGenerator = Depends(get_jwt_token_generator),
) -> IssuedJWTTokensOut:
    device_id = token_generator.get_device_id()
    access, refresh = await update_tokens_use_case.execute(
        form.refresh_token, device_id
    )
    return IssuedJWTTokensOut(
        access_token=access, refresh_token=refresh, exp=jwttoken_service.access_ttl_sec
    )


@router.get(
    path="/logout",
    summary="Revoke token",
)
async def revorke_token(
    authorization_header: AuthAPIHeaderIn,
    header_verify: AuthHeaderVerifyUtils = Depends(get_auth_header_verify),
    logout_use_case: LogoutUseCase = Depends(get_logout_use_case),
) -> UserActionOut:
    token = header_verify.verify(authorization_header)
    await logout_use_case.execute(token)
    return UserActionOut()


@router.get(
    path="/full-logout",
    summary="Revoke all tokens",
)
async def revorke_all_tokens(
    authorization_header: AuthAPIHeaderIn,
    header_verify: AuthHeaderVerifyUtils = Depends(get_auth_header_verify),
    full_logout_use_case: FullLogoutUseCase = Depends(get_full_logout_use_case),
) -> UserActionOut:
    token = header_verify.verify(authorization_header)
    await full_logout_use_case.execute(token)
    return UserActionOut()
