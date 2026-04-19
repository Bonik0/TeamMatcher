from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from email_service.app.email_verify.use_cases.save_code import (
    SaveVerificationCodeUseCase,
)
from email_service.app.email_verify.use_cases.verify_code import VerifyCodeUseCase
from email_service.app.email_verify.use_cases.success_verify import SuccessVerifyUseCase
from core.entities import VerificationCode
from fastapi.exceptions import HTTPException


@pytest.mark.asyncio
async def test_save_verification_code_calls_repo_and_publisher() -> None:
    repo = AsyncMock()
    publisher = AsyncMock()
    use_case = SaveVerificationCodeUseCase(repo, publisher, code_lifetime=300)

    op_id = uuid4()
    result = await use_case.execute("user@example.com", 1234, op_id)

    assert isinstance(result, VerificationCode)
    assert result.email == "user@example.com"
    repo.save.assert_awaited_once()
    publisher.publish.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_verify_code_branches() -> None:
    op_id = uuid4()
    repo = AsyncMock()
    repo.find_by_email = AsyncMock(return_value=None)
    use_case = VerifyCodeUseCase(repo, max_attempts=3)
    with pytest.raises(HTTPException):
        await use_case.execute("a@a.com", 1111, op_id)

    vc = VerificationCode(
        email="a@a.com", code=2222, operation_id=op_id, attempt_count=5
    )
    repo.find_by_email = AsyncMock(return_value=vc)
    use_case = VerifyCodeUseCase(repo, max_attempts=3)
    with pytest.raises(HTTPException):
        await use_case.execute("a@a.com", 2222, op_id)

    vc = VerificationCode(
        email="a@a.com", code=2222, operation_id=uuid4(), attempt_count=0
    )
    repo.find_by_email = AsyncMock(return_value=vc)
    use_case = VerifyCodeUseCase(repo, max_attempts=3)
    with pytest.raises(HTTPException):
        await use_case.execute("a@a.com", 2222, op_id)

    vc = VerificationCode(
        email="b@b.com", code=3333, operation_id=op_id, attempt_count=0
    )
    repo.find_by_email = AsyncMock(return_value=vc)
    use_case = VerifyCodeUseCase(repo, max_attempts=3)
    ok, found = await use_case.execute("b@b.com", 3333, op_id)
    assert ok is True
    assert found.email == "b@b.com"

    vc = VerificationCode(
        email="c@c.com", code=4444, operation_id=op_id, attempt_count=0
    )
    repo.find_by_email = AsyncMock(return_value=vc)
    repo.increment_attempts = AsyncMock()
    use_case = VerifyCodeUseCase(repo, max_attempts=3)
    ok, found = await use_case.execute("c@c.com", 9999, op_id)
    assert ok is False
    repo.increment_attempts.assert_awaited_once_with("c@c.com")


@pytest.mark.asyncio
async def test_success_verify_deletes_and_publishes() -> None:
    repo = AsyncMock()
    publisher = AsyncMock()
    use_case = SuccessVerifyUseCase(publisher, repo)

    vc = VerificationCode(email="x@y.com", code=1111, operation_id=uuid4())
    await use_case.execute(vc)

    repo.delete.assert_awaited_once_with("x@y.com")
    publisher.publish.assert_awaited_once_with(vc)
