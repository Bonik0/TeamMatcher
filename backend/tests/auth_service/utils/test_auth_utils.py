import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from auth_service.app.auth.utils import login_key_executor


@pytest.mark.asyncio
async def test_login_key_executor_extracts_email():
    req = SimpleNamespace()
    req.json = AsyncMock(return_value={"email": "u@e.com"})
    req.url = SimpleNamespace(path="/login")

    keys = await login_key_executor(req)
    assert keys == ["/login", "email", "u@e.com"]


@pytest.mark.asyncio
async def test_login_key_executor_empty_if_no_email():
    req = SimpleNamespace()
    req.json = AsyncMock(return_value={"a": 1})
    req.url = SimpleNamespace(path="/login")

    keys = await login_key_executor(req)
    assert keys == []


@pytest.mark.asyncio
async def test_login_key_executor_empty_if_no_body():
    req = SimpleNamespace()
    req.url = SimpleNamespace(path="/login")

    keys = await login_key_executor(req)
    assert keys == []
