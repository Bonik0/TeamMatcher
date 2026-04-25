from core.interfaces.repositories.token_black_list import IBlacklistRepository
from core.entities import JWTTokenType
from datetime import datetime
from app.jwttoken.user_cases.validate_token_use_case import ValidateTokenUseCase
from app.jwttoken.utils import JWTService
from core.interfaces.use_case import IUseCase


class FullLogoutUseCase(IUseCase):
    def __init__(
        self,
        jwttoken_service: JWTService,
        repository: IBlacklistRepository,
        validate_token_use_case: ValidateTokenUseCase,
    ) -> None:
        self.repository = repository
        self.validate_token_use_case = validate_token_use_case
        self.jwttoken_service = jwttoken_service

    async def execute(self, token: str) -> None:
        payload = await self.validate_token_use_case.execute(token, JWTTokenType.ACCESS)

        user_id = payload.user_id
        timestamp = int(datetime.now().timestamp())
        ttl = int(self.jwttoken_service.refresh_ttl_sec)

        await self.repository.set_user_revocation_timestamp(user_id, timestamp, ttl)
