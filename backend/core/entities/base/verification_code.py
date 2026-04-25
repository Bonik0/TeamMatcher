from uuid import UUID
from pydantic import PositiveInt, EmailStr, BaseModel, Field
from datetime import datetime


class VerificationCode(BaseModel):
    email: EmailStr
    code: PositiveInt
    operation_id: UUID
    attempt_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

    def is_expired(self, lifetime_seconds: int) -> bool:
        return (datetime.now() - self.created_at).seconds > lifetime_seconds

    def increment_attempts(self) -> None:
        self.attempt_count += 1

    def has_exceeded_attempts(self, max_attempts: int) -> bool:
        return self.attempt_count >= max_attempts
