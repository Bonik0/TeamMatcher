from uuid import UUID
from pydantic import EmailStr
from core.entities import VerificationCode
from redis.asyncio import Redis
from core.interfaces.repositories.verification_code import IVerificationRepository


class RedisVerificationRepository(IVerificationRepository):
    def __init__(self, client: Redis) -> None:
        self.client = client

    @staticmethod
    def _get_key(email: EmailStr) -> str:
        return f"code:{email}"

    @staticmethod
    def _get_code_key() -> str:
        return "code"

    @staticmethod
    def _get_attempt_count_key() -> str:
        return "attempt_count"

    @staticmethod
    def _get_op_id_key() -> str:
        return "op_id"

    async def save(
        self, verification_code: VerificationCode, lifetime_seconds: int
    ) -> None:
        key = self._get_key(verification_code.email)

        async with self.client.pipeline() as pipeline:
            pipeline.multi()
            code_value = {
                self._get_code_key(): verification_code.code,
                self._get_op_id_key(): str(verification_code.operation_id),
                self._get_attempt_count_key(): verification_code.attempt_count,
            }
            pipeline.hmset(key, mapping=code_value)
            pipeline.expire(key, lifetime_seconds)
            await pipeline.execute()

    async def delete(self, email: EmailStr) -> None:
        await self.client.delete(self._get_key(email))

    async def find_by_email(self, email: EmailStr) -> VerificationCode | None:
        key = self._get_key(email)
        correct_code_key = self._get_code_key()
        attempt_count_key = self._get_attempt_count_key()
        op_id_key = self._get_op_id_key()

        correct_code, attempt_count, correct_op_id = await self.client.hmget(
            key, correct_code_key, attempt_count_key, op_id_key
        )

        if correct_code is None or attempt_count is None or correct_op_id is None:
            return None

        return VerificationCode(
            email=email,
            code=int(correct_code),
            operation_id=UUID(correct_op_id.decode()),
            attempt_count=int(attempt_count),
        )

    async def increment_attempts(self, email: EmailStr) -> None:
        key = self._get_key(email)
        await self.client.hincrby(key, self._get_attempt_count_key())
