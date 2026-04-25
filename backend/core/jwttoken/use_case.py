from core.jwttoken.schemas import AuthAPIHeaderIn

from fastapi import HTTPException, status
import aiohttp
from typing import Any
from core.entities import JWTTokenPayload, UserRoleType
from core.interfaces.use_case import IUseCase


class UserVerifyUseCase(IUseCase):
    def __init__(
        self,
        service_url: str,
        verify_endpoint_method: str,
        session: aiohttp.ClientSession,
    ) -> None:
        self.service_url = service_url
        self.verify_endpoint_method = verify_endpoint_method
        self.session = session

    async def execute(
        self, auth_header: AuthAPIHeaderIn, *user_roles: UserRoleType
    ) -> JWTTokenPayload:

        if auth_header is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Need bearer token"
            )

        response = await self.session.request(
            self.verify_endpoint_method,
            self.service_url,
            headers={"Authorization": auth_header},
        )
        response_json: dict[str, Any] = await response.json()

        if response.status != 200:
            raise HTTPException(
                status_code=response.status, detail=response_json["detail"]
            )

        payload = JWTTokenPayload.model_validate(response_json)

        if payload.role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only roles: {user_roles} have access",
            )
        return payload
