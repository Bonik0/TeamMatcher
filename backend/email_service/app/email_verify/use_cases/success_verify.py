from faststream.rabbit.publisher import RabbitPublisher
from core.entities import VerificationCode
from core.interfaces.repositories.verification_code import IVerificationRepository
from core.interfaces.use_case import IUseCase


class SuccessVerifyUseCase(IUseCase):
    def __init__(
        self, publisher: RabbitPublisher, repository: IVerificationRepository
    ) -> None:
        self.publisher = publisher
        self.repository = repository

    async def execute(self, code: VerificationCode) -> None:
        await self.repository.delete(code.email)
        await self.publisher.publish(code)
