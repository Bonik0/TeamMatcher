from fastapi import APIRouter, Depends
from app.auth.schemas import (
    UserRegistrationCredentialsIn,
    UserLoginCredentialsIn,
    UserChangePasswordIn,
)
from core.schemas import UpdateUserActionOut
from app.auth.use_cases.login_case import LoginUserUseCase
from app.auth.use_cases.change_password_case import ChangePasswordUseCase
from app.auth.use_cases.register_case import RegisterUserUseCase
from app.auth.dependencies.use_cases import (
    get_change_password_user_case,
    get_login_user_case,
    get_register_use_case,
)
from core.entities import UserRoleType
from app.jwttoken.dependencies.user_cases import get_generate_tokens_use_case
from app.jwttoken.user_cases.generate_token_case import GenerateTokensUseCase
from app.jwttoken.utils import JWTGenerator
from app.jwttoken.dependencies.utils import get_jwt_token_generator
from core.jwttoken.schemas import IssuedJWTTokensOut
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies.postgres import get_session


router = APIRouter(
    tags=["Authentication"],
)


@router.post(
    path="/registration",
    summary="User registration",
)
async def user_registrate(
    user_credentials: UserRegistrationCredentialsIn,
    register_use_case: RegisterUserUseCase = Depends(get_register_use_case),
    generate_tokens_use_case: GenerateTokensUseCase = Depends(
        get_generate_tokens_use_case
    ),
    jwt_token_generator: JWTGenerator = Depends(get_jwt_token_generator),
    session: AsyncSession = Depends(get_session),
) -> IssuedJWTTokensOut:
    user_id = await register_use_case.execute(
        session, user_credentials, UserRoleType.user
    )
    device_id = jwt_token_generator.get_device_id()
    access, refresh = await generate_tokens_use_case.execute(
        user_id, UserRoleType.user, device_id
    )
    return IssuedJWTTokensOut(
        access_token=access,
        refresh_token=refresh,
        exp=generate_tokens_use_case.jwt_service.access_ttl_sec,
    )


@router.post(
    path="/organizer-registration",
    summary="Organizer registration",
)
async def organizer_registrate(
    organizer_credentials: UserRegistrationCredentialsIn,
    register_use_case: RegisterUserUseCase = Depends(get_register_use_case),
    generate_tokens_use_case: GenerateTokensUseCase = Depends(
        get_generate_tokens_use_case
    ),
    jwt_token_generator: JWTGenerator = Depends(get_jwt_token_generator),
    session: AsyncSession = Depends(get_session),
) -> IssuedJWTTokensOut:
    user_id = await register_use_case.execute(
        session, organizer_credentials, UserRoleType.organizer
    )
    device_id = jwt_token_generator.get_device_id()
    access, refresh = await generate_tokens_use_case.execute(
        user_id, UserRoleType.organizer, device_id
    )
    return IssuedJWTTokensOut(
        access_token=access,
        refresh_token=refresh,
        exp=generate_tokens_use_case.jwt_service.access_ttl_sec,
    )


@router.post(
    path="/login",
    summary="Sign in to account",
)
async def login(
    user_credentials: UserLoginCredentialsIn,
    login_use_case: LoginUserUseCase = Depends(get_login_user_case),
    generate_tokens_use_case: GenerateTokensUseCase = Depends(
        get_generate_tokens_use_case
    ),
    jwt_token_generator: JWTGenerator = Depends(get_jwt_token_generator),
    session: AsyncSession = Depends(get_session),
) -> IssuedJWTTokensOut:
    user = await login_use_case.execute(session, user_credentials)
    device_id = jwt_token_generator.get_device_id()
    access, refresh = await generate_tokens_use_case.execute(
        user.id, user.role, device_id
    )
    return IssuedJWTTokensOut(
        access_token=access,
        refresh_token=refresh,
        exp=generate_tokens_use_case.jwt_service.access_ttl_sec,
    )


@router.post(
    path="/change-password",
    summary="Change password",
)
async def change_password(
    user_credentials: UserChangePasswordIn,
    change_password_case: ChangePasswordUseCase = Depends(
        get_change_password_user_case
    ),
    session: AsyncSession = Depends(get_session),
) -> UpdateUserActionOut:
    await change_password_case.execute(
        session,
        user_credentials.email,
        user_credentials.operation_id,
        user_credentials.password,
    )
    return UpdateUserActionOut()
