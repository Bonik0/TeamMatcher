from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from auth_service.app.auth.use_cases.login_case import LoginUserUseCase
from auth_service.app.auth.use_cases.register_case import RegisterUserUseCase
from auth_service.app.auth.use_cases.change_password_case import ChangePasswordUseCase
from auth_service.app.jwttoken.user_cases.validate_token_use_case import (
    ValidateTokenUseCase,
)
from auth_service.app.jwttoken.user_cases.generate_token_case import (
    GenerateTokensUseCase,
)
from auth_service.app.jwttoken.user_cases.logout_use_case import LogoutUseCase
from auth_service.app.jwttoken.user_cases.full_logout_use_case import FullLogoutUseCase
from core.entities import JWTTokenPayload, JWTTokenType, UserRoleType
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_login_user_success_and_failures():
    repo = AsyncMock()
    hashing = MagicMock()
    hashing.verify_password.return_value = True
    user = SimpleNamespace(id=1, email="a@a.com", hash_password="h")
    repo.get_by_email = AsyncMock(return_value=user)

    use_case = LoginUserUseCase(repo, hashing)
    session = AsyncMock()
    creds = SimpleNamespace(email="a@a.com", password="p")

    res = await use_case.execute(session, creds)
    assert res == user

    repo.get_by_email = AsyncMock(return_value=None)
    with pytest.raises(HTTPException):
        await use_case.execute(session, creds)

    repo.get_by_email = AsyncMock(return_value=user)
    hashing.verify_password.return_value = False
    with pytest.raises(HTTPException):
        await use_case.execute(session, creds)


@pytest.mark.asyncio
async def test_register_user_branches_and_success():
    repo = AsyncMock()
    hashing = MagicMock()
    verification = AsyncMock()
    logger = MagicMock()

    cred = SimpleNamespace(
        email="u@e.com",
        password="p",
        first_name="F",
        patronymic=None,
        surname="S",
        operation_id=uuid4(),
    )

    repo.get_by_email = AsyncMock(return_value=SimpleNamespace(id=1))
    use_case = RegisterUserUseCase(repo, hashing, verification, logger)
    session = AsyncMock()
    with pytest.raises(HTTPException):
        await use_case.execute(session, cred, UserRoleType.user)

    repo.get_by_email = AsyncMock(return_value=None)
    verification.exist = AsyncMock(return_value=False)
    with pytest.raises(HTTPException):
        await use_case.execute(session, cred, UserRoleType.user)

    verification.exist = AsyncMock(return_value=True)
    repo.create = AsyncMock(return_value=42)
    session.commit = AsyncMock()
    verification.delete = AsyncMock()
    user_id = await use_case.execute(session, cred, UserRoleType.user)
    assert user_id == 42
    session.commit.assert_awaited_once()
    verification.delete.assert_awaited_once_with(cred.email, cred.operation_id)


@pytest.mark.asyncio
async def test_change_password_branches_and_success():
    repo = AsyncMock()
    hashing = MagicMock()
    verification = AsyncMock()
    logger = MagicMock()
    session = AsyncMock()

    use_case = ChangePasswordUseCase(repo, hashing, verification, logger)

    repo.get_by_email = AsyncMock(return_value=None)
    with pytest.raises(HTTPException):
        await use_case.execute(session, "x@y", uuid4(), "new")

    repo.get_by_email = AsyncMock(return_value=SimpleNamespace(id=1, email="x@y"))
    verification.exist = AsyncMock(return_value=False)
    with pytest.raises(HTTPException):
        await use_case.execute(session, "x@y", uuid4(), "new")

    verification.exist = AsyncMock(return_value=True)
    repo.update_password = AsyncMock()
    verification.delete = AsyncMock()
    session.commit = AsyncMock()
    user = SimpleNamespace(id=1, email="x@y")
    repo.get_by_email = AsyncMock(return_value=user)
    res = await use_case.execute(session, "x@y", uuid4(), "newpass")
    assert res == user
    verification.delete.assert_awaited()
    session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_validate_generate_and_logout_use_cases():
    jwt_service = MagicMock()
    repo = AsyncMock()
    from uuid import uuid4 as _uuid4

    payload = JWTTokenPayload(
        jti="j",
        user_id=5,
        device_id=str(_uuid4()),
        role=UserRoleType.user,
        type=JWTTokenType.ACCESS,
        exp=datetime.now() + timedelta(seconds=10),
        iat=datetime.now(),
    )
    jwt_service.decode_token.return_value = payload
    repo.is_device_blacklisted = AsyncMock(return_value=False)
    repo.get_user_revocation_timestamp = AsyncMock(return_value=None)
    validate = ValidateTokenUseCase(jwt_service, repo)
    res = await validate.execute("token", JWTTokenType.ACCESS)
    assert res.user_id == 5

    gen = GenerateTokensUseCase(jwt_service)
    tokens = await gen.execute(1, UserRoleType.user, uuid4())
    assert isinstance(tokens, tuple) and len(tokens) == 2

    repo.add_device_to_blacklist = AsyncMock()
    logout_validate = MagicMock()
    logout_validate.execute = AsyncMock(return_value=payload)
    logout = LogoutUseCase(repo, logout_validate)
    await logout.execute("token")
    repo.add_device_to_blacklist.assert_awaited()

    full = FullLogoutUseCase(jwt_service, repo, logout_validate)
    jwt_service.refresh_ttl_sec = 300
    repo.set_user_revocation_timestamp = AsyncMock()
    await full.execute("token")
    repo.set_user_revocation_timestamp.assert_awaited_once()
