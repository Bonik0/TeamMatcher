from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from email_service.app.email_verify.utils import (
    EmailVerifyUtils,
    email_verify_key_executor,
)


@pytest.mark.asyncio
async def test_email_verify_key_executor_returns_email_key_when_present() -> None:
    req = SimpleNamespace()
    req.json = AsyncMock(return_value={"email": "u@e.com"})
    req.url = SimpleNamespace(path="/verify")

    keys = await email_verify_key_executor(req)
    assert keys == ["/verify", "email", "u@e.com"]


@pytest.mark.asyncio
async def test_email_verify_key_executor_returns_empty_when_no_email() -> None:
    req = SimpleNamespace()
    req.json = AsyncMock(return_value={"foo": "bar"})
    req.url = SimpleNamespace(path="/verify")

    keys = await email_verify_key_executor(req)
    assert keys == []


@pytest.mark.asyncio
async def test_email_verify_key_executor_returns_if_no_body() -> None:
    req = SimpleNamespace()
    req.url = SimpleNamespace(path="/verify")

    keys = await email_verify_key_executor(req)
    assert keys == []


def test_email_verify_utils_generates_code_in_range_and_operation_id(
    monkeypatch,
) -> None:
    ev = EmailVerifyUtils(code_length=4)
    with patch(
        "email_service.app.email_verify.utils.random.randint", return_value=1000
    ):
        code = ev.generate_code()
        assert code == 1000

    fixed = UUID("00000000-0000-0000-0000-000000000001")
    with patch("email_service.app.email_verify.utils.uuid4", return_value=fixed):
        op = ev.generate_operation_id()
        assert op == fixed
