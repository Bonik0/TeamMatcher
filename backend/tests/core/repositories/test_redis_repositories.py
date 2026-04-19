from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from core.entities import VerificationCode
from core.repositories.rate_limiter import RedisRateLimiterRepository
from core.repositories.token_black_list import RedisBlacklistRepository
from core.repositories.user_verification import RedisUserVerificationRepository
from core.repositories.verification_code import RedisVerificationRepository


def _make_pipeline() -> MagicMock:
    pipeline = MagicMock()
    pipeline.execute = AsyncMock()
    return pipeline


@pytest.mark.asyncio
async def test_rate_limiter_repository_returns_block_status_and_ttl() -> None:
    client = AsyncMock()
    client.exists.return_value = 1
    client.ttl.return_value = 42

    repository = RedisRateLimiterRepository(client)

    assert await repository.is_blocked(["ip", "127.0.0.1"]) == (True, 42)
    client.exists.assert_awaited_once_with("rate_limit:ip:127.0.0.1:blocked")
    client.ttl.assert_awaited_once_with("rate_limit:ip:127.0.0.1:blocked")


@pytest.mark.asyncio
async def test_rate_limiter_repository_sets_expire_only_for_first_attempt() -> None:
    client = AsyncMock()
    client.incr.return_value = 1

    repository = RedisRateLimiterRepository(client)

    attempt = await repository.increment_count(["user", "1"], period=60)

    assert attempt == 1
    client.expire.assert_awaited_once_with("rate_limit:user:1:count", 60)


@pytest.mark.asyncio
async def test_rate_limiter_repository_does_not_reset_ttl_for_existing_counter() -> (
    None
):
    client = AsyncMock()
    client.incr.return_value = 3

    repository = RedisRateLimiterRepository(client)

    attempt = await repository.increment_count(["user", "1"], period=60)

    assert attempt == 3
    client.expire.assert_not_awaited()


@pytest.mark.asyncio
async def test_rate_limiter_repository_blocks_and_resets_keys() -> None:
    client = AsyncMock()
    repository = RedisRateLimiterRepository(client)

    await repository.block(["ip", "127.0.0.1"], block_time=120)
    await repository.reset_count(["ip", "127.0.0.1"])

    client.setex.assert_awaited_once_with("rate_limit:ip:127.0.0.1:blocked", 120, 1)
    client.delete.assert_awaited_once_with("rate_limit:ip:127.0.0.1:count")


@pytest.mark.asyncio
async def test_blacklist_repository_adds_and_reads_device_blacklist() -> None:
    device_id = uuid4()
    client = AsyncMock()
    client.exists.return_value = 1
    repository = RedisBlacklistRepository(client)

    assert await repository.add_device_to_blacklist(device_id, ttl=300) is True
    assert await repository.is_device_blacklisted(device_id) is True

    key = f"blacklist:device_id:{device_id}"
    client.setex.assert_awaited_once_with(key, 300, "revoked")
    client.exists.assert_awaited_once_with(key)


@pytest.mark.asyncio
async def test_blacklist_repository_returns_none_when_revocation_timestamp_missing() -> (
    None
):
    client = AsyncMock()
    client.get.return_value = None
    repository = RedisBlacklistRepository(client)

    assert await repository.get_user_revocation_timestamp(5) is None


@pytest.mark.asyncio
async def test_blacklist_repository_reads_revocation_timestamp() -> None:
    client = AsyncMock()
    client.get.return_value = b"1700000000"
    repository = RedisBlacklistRepository(client)

    await repository.set_user_revocation_timestamp(5, timestamp=1700000000, ttl=60)

    assert await repository.get_user_revocation_timestamp(5) == 1700000000
    client.setex.assert_awaited_once_with("blacklist:user:5", 60, 1700000000)


@pytest.mark.asyncio
async def test_user_verification_repository_saves_deletes_and_checks_existence() -> (
    None
):
    op_id = uuid4()
    email = "user@example.com"
    client = AsyncMock()
    client.delete.return_value = 1
    client.exists.return_value = 1
    repository = RedisUserVerificationRepository(client)

    await repository.save(email, op_id, lifetime_seconds=180)

    assert await repository.delete(email, op_id) is True
    assert await repository.exist(email, op_id) is True

    key = f"verify:{email}:{op_id}"
    client.set.assert_awaited_once_with(key, 0, 180)
    client.delete.assert_awaited_once_with(key)
    client.exists.assert_awaited_once_with(key)


@pytest.mark.asyncio
async def test_verification_code_repository_saves_code_via_pipeline() -> None:
    verification_code = VerificationCode(
        email="user@example.com",
        code=123456,
        operation_id=uuid4(),
    )
    pipeline = _make_pipeline()
    client = MagicMock()
    pipeline_cm = MagicMock()
    pipeline_cm.__aenter__ = AsyncMock(return_value=pipeline)
    pipeline_cm.__aexit__ = AsyncMock(return_value=None)
    client.pipeline.return_value = pipeline_cm
    repository = RedisVerificationRepository(client)

    await repository.save(verification_code, lifetime_seconds=300)

    key = "code:user@example.com"
    pipeline.multi.assert_called_once_with()
    pipeline.hmset.assert_called_once_with(
        key,
        mapping={
            "code": 123456,
            "op_id": str(verification_code.operation_id),
            "attempt_count": 0,
        },
    )
    pipeline.expire.assert_called_once_with(key, 300)
    pipeline.execute.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_verification_code_repository_returns_none_when_code_is_incomplete() -> (
    None
):
    client = AsyncMock()
    client.hmget.return_value = (
        b"123456",
        None,
        b"550e8400-e29b-41d4-a716-446655440000",
    )
    repository = RedisVerificationRepository(client)

    assert await repository.find_by_email("user@example.com") is None


@pytest.mark.asyncio
async def test_verification_code_repository_restores_entity_from_redis() -> None:
    operation_id = uuid4()
    client = AsyncMock()
    client.hmget.return_value = (
        b"123456",
        b"2",
        str(operation_id).encode(),
    )
    repository = RedisVerificationRepository(client)

    verification_code = await repository.find_by_email("user@example.com")

    assert verification_code is not None
    assert verification_code.email == "user@example.com"
    assert verification_code.code == 123456
    assert verification_code.operation_id == operation_id
    assert verification_code.attempt_count == 2


@pytest.mark.asyncio
async def test_verification_code_repository_deletes_and_increments_attempts() -> None:
    client = AsyncMock()
    repository = RedisVerificationRepository(client)

    await repository.delete("user@example.com")
    await repository.increment_attempts("user@example.com")

    client.delete.assert_awaited_once_with("code:user@example.com")
    client.hincrby.assert_awaited_once_with("code:user@example.com", "attempt_count")
