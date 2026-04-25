from core.interfaces.repositories.token_black_list import IBlacklistRepository
from uuid import UUID
from core.entities import JWTTokenType
from datetime import datetime
from app.jwttoken.user_cases.validate_token_use_case import ValidateTokenUseCase
from core.interfaces.use_case import IUseCase


class LogoutUseCase(IUseCase):
    def __init__(
        self,
        repository: IBlacklistRepository,
        validate_token_use_case: ValidateTokenUseCase,
    ) -> None:
        self.repository = repository
        self.validate_token_use_case = validate_token_use_case

    async def execute(self, token: str) -> None:
        payload = await self.validate_token_use_case.execute(token, JWTTokenType.ACCESS)

        device_id = UUID(payload.device_id)
        block_ttl = int(payload.exp.timestamp() - datetime.now().timestamp())

        await self.repository.add_device_to_blacklist(device_id, block_ttl)
