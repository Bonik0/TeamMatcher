from uuid import UUID
from pydantic import PositiveInt, EmailStr
from core.entities import VerificationCode
from core.interfaces.repositories.verification_code import IVerificationRepository
from faststream.rabbit.publisher import RabbitPublisher
from core.interfaces.use_case import IUseCase


class SaveVerificationCodeUseCase(IUseCase):
    def __init__(
        self,
        repository: IVerificationRepository,
        publisher: RabbitPublisher,
        code_lifetime: int,
    ) -> None:
        self.repository = repository
        self.code_lifetime = code_lifetime
        self.publisher = publisher

    async def execute(
        self, email: EmailStr, code: PositiveInt, operation_id: UUID
    ) -> VerificationCode:
        verification_code = VerificationCode(
            email=email, code=code, operation_id=operation_id
        )
        await self.repository.save(verification_code, self.code_lifetime)
        await self.publisher.publish(verification_code)

        return verification_code
