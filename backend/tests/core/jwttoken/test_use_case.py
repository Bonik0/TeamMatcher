from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status

from core.entities import JWTTokenType, UserRoleType
from core.jwttoken.use_case import UserVerifyUseCase


@pytest.mark.asyncio
async def test_user_verify_use_case_requires_authorization_header() -> None:
    use_case = UserVerifyUseCase("http://auth/verify", "GET", AsyncMock())

    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(None, UserRoleType.user)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Need bearer token"


@pytest.mark.asyncio
async def test_user_verify_use_case_propagates_remote_error() -> None:
    response = AsyncMock()
    response.status = 401
    response.json.return_value = {"detail": "Invalid token"}
    session = AsyncMock()
    session.request.return_value = response
    use_case = UserVerifyUseCase("http://auth/verify", "POST", session)

    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute("Bearer token", UserRoleType.user)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
    session.request.assert_awaited_once_with(
        "POST",
        "http://auth/verify",
        headers={"Authorization": "Bearer token"},
    )


@pytest.mark.asyncio
async def test_user_verify_use_case_rejects_role_without_access() -> None:
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {
        "jti": "jti",
        "user_id": 1,
        "device_id": "device",
        "role": UserRoleType.organizer,
        "type": JWTTokenType.ACCESS,
        "exp": datetime.now().isoformat(),
        "iat": datetime.now().isoformat(),
    }
    session = AsyncMock()
    session.request.return_value = response
    use_case = UserVerifyUseCase("http://auth/verify", "GET", session)

    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute("Bearer token", UserRoleType.user)

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == f"Only roles: {(UserRoleType.user,)} have access"


@pytest.mark.asyncio
async def test_user_verify_use_case_returns_payload_for_allowed_role() -> None:
    now = datetime.now().isoformat()
    response = AsyncMock()
    response.status = 200
    response.json.return_value = {
        "jti": "jti",
        "user_id": 1,
        "device_id": "device",
        "role": UserRoleType.user,
        "type": JWTTokenType.ACCESS,
        "exp": now,
        "iat": now,
    }
    session = AsyncMock()
    session.request.return_value = response
    use_case = UserVerifyUseCase("http://auth/verify", "GET", session)

    payload = await use_case.execute("Bearer token", UserRoleType.user)

    assert payload.user_id == 1
    assert payload.role == UserRoleType.user
    assert payload.type == JWTTokenType.ACCESS
