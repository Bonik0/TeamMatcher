from pydantic import PositiveInt
import random
from uuid import UUID, uuid4
from fastapi import Request


async def email_verify_key_executor(request: Request) -> list[str]:
    body = await request.json()
    email = body.get("email")
    return [request.url.path, "email", email] if email is not None else []


class EmailVerifyUtils:
    def __init__(
        self,
        code_length: PositiveInt,
    ) -> None:
        self.code_length = code_length

    def generate_code(self) -> PositiveInt:
        min_value = 10 ** (self.code_length - 1)
        max_value = (10**self.code_length) - 1

        return random.randint(min_value, max_value)

    def generate_operation_id(self) -> UUID:
        return uuid4()
