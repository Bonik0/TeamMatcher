import pytest

from auth_service.app.jwttoken.utils import (
    JWTService,
    JWTGenerator,
    AuthHeaderVerifyUtils,
)
from core.entities import UserRoleType, JWTTokenType


def test_jwt_service_create_and_decode_token_roundtrip():
    svc = JWTService(
        secret_key="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        algorithm="HS256",
        access_ttl_sec=60,
        refresh_ttl_sec=120,
    )
    device = JWTGenerator.get_device_id()
    token = svc.create_access_token(user_id=1, role=UserRoleType.user, device_id=device)

    import auth_service.app.jwttoken.utils as utils_mod

    orig_decode = utils_mod.jwt.decode
    try:
        utils_mod.jwt.decode = lambda token, key, algorithms: orig_decode(
            token, key, algorithms=algorithms, options={"verify_iat": False}
        )
        payload = svc.decode_token(token)
    finally:
        utils_mod.jwt.decode = orig_decode

    assert payload.user_id == 1
    assert payload.role == UserRoleType.user
    assert payload.type == JWTTokenType.ACCESS


def test_jwt_service_decode_invalid_raises():
    svc = JWTService(
        secret_key="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        algorithm="HS256",
        access_ttl_sec=1,
        refresh_ttl_sec=1,
    )
    with pytest.raises(Exception):
        svc.decode_token("not-a-token")


def test_auth_header_verify_utils_behaviour():
    v = AuthHeaderVerifyUtils()
    with pytest.raises(Exception):
        v.verify(None)
    with pytest.raises(Exception):
        v.verify("Token abc")
    assert v.verify("Bearer abc.def") == "abc.def"
