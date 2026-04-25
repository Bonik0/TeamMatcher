from fastapi import Depends
from core.jwttoken.config import (
    AuthtorizationServiceSettings,
    get_auth_service_settings,
)
from core.jwttoken.use_case import UserVerifyUseCase
import aiohttp
from typing import AsyncGenerator
from core.entities import UserRoleType
from typing import Callable
from fastapi import Request, params
from core.jwttoken.schemas import AuthAPIHeaderIn


async def get_user_verify_use_case(
    settings: AuthtorizationServiceSettings = Depends(get_auth_service_settings),
) -> AsyncGenerator[UserVerifyUseCase, None]:
    async with aiohttp.ClientSession() as session:
        yield UserVerifyUseCase(settings.URL, settings.METHOD, session)


def get_verifier(
    *user_roles: UserRoleType,
) -> Callable[[Request, str, UserVerifyUseCase], params.Depends]:

    async def verify(
        request: Request,
        header: AuthAPIHeaderIn,
        use_case: UserVerifyUseCase = Depends(get_user_verify_use_case),
    ) -> None:
        payload = await use_case.execute(header, *user_roles)
        request.state.user_id = payload.user_id
        request.state.role = payload.role

    return Depends(verify)
