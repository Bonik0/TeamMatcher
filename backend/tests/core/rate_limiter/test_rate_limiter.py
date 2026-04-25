import json
import logging
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from core.rate_limiter.middleware import RateLimitMiddleware
from core.rate_limiter.schemas import EndpointConfig
from core.rate_limiter.use_case import RateLimitUseCase
from core.rate_limiter.utils import extract_ip


def _make_request(
    path: str = "/limited",
    headers: list[tuple[bytes, bytes]] | None = None,
    client_host: str = "127.0.0.1",
) -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "headers": headers or [],
        "client": (client_host, 12345),
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
    }
    return Request(scope)


@pytest.mark.asyncio
async def test_rate_limit_use_case_rejects_blocked_keys() -> None:
    repository = AsyncMock()
    repository.is_blocked.return_value = (True, 55)
    logger = Mock(spec=logging.Logger)
    use_case = RateLimitUseCase(repository, logger)

    allowed, ttl = await use_case.allow_request(
        keys=["ip", "127.0.0.1"],
        limit=5,
        period=60,
        block_time=120,
    )

    assert (allowed, ttl) == (False, 55)
    repository.increment_count.assert_not_awaited()
    logger.info.assert_called_once_with("key=['ip', '127.0.0.1'] is blocked, ttl=55")


@pytest.mark.asyncio
async def test_rate_limit_use_case_blocks_after_limit_is_reached() -> None:
    repository = AsyncMock()
    repository.is_blocked.return_value = (False, 0)
    repository.increment_count.return_value = 3
    logger = Mock(spec=logging.Logger)
    use_case = RateLimitUseCase(repository, logger)

    allowed, ttl = await use_case.allow_request(
        keys=["ip", "127.0.0.1"],
        limit=3,
        period=60,
        block_time=120,
    )

    assert (allowed, ttl) == (True, 0)
    repository.block.assert_awaited_once_with(["ip", "127.0.0.1"], 120)
    repository.reset_count.assert_awaited_once_with(["ip", "127.0.0.1"])
    assert (
        logger.info.call_args_list[0].args[0] == "block key=['ip', '127.0.0.1'] for 120"
    )
    assert logger.info.call_args_list[1].args[0] == "OK for key=['ip', '127.0.0.1']"


@pytest.mark.asyncio
async def test_rate_limit_use_case_allows_request_below_limit() -> None:
    repository = AsyncMock()
    repository.is_blocked.return_value = (False, 0)
    repository.increment_count.return_value = 2
    logger = Mock(spec=logging.Logger)
    use_case = RateLimitUseCase(repository, logger)

    allowed, ttl = await use_case.allow_request(
        keys=["ip", "127.0.0.1"],
        limit=3,
        period=60,
        block_time=120,
    )

    assert (allowed, ttl) == (True, 0)
    repository.block.assert_not_awaited()
    repository.reset_count.assert_not_awaited()
    logger.info.assert_called_once_with("OK for key=['ip', '127.0.0.1']")


@pytest.mark.asyncio
async def test_rate_limit_middleware_skips_unconfigured_endpoints() -> None:
    use_case = AsyncMock()
    middleware = RateLimitMiddleware(FastAPI(), use_case, endpoint_configs={})
    request = _make_request(path="/free")
    response = Response(status_code=204)
    call_next = AsyncMock(return_value=response)

    result = await middleware.dispatch(request, call_next)

    assert result is response
    call_next.assert_awaited_once_with(request)
    use_case.allow_request.assert_not_awaited()


@pytest.mark.asyncio
async def test_rate_limit_middleware_uses_default_extractor_and_allows_request() -> (
    None
):
    use_case = AsyncMock()
    use_case.allow_request.return_value = (True, 0)
    middleware = RateLimitMiddleware(
        FastAPI(),
        use_case,
        endpoint_configs={
            "/limited": EndpointConfig(
                limit=5,
                period=60,
                block_time=120,
                key_extractor=None,
            )
        },
    )
    request = _make_request(path="/limited", client_host="10.0.0.1")
    response = Response(status_code=200)
    call_next = AsyncMock(return_value=response)

    result = await middleware.dispatch(request, call_next)

    assert result is response
    use_case.allow_request.assert_awaited_once_with(
        keys=["ip", "10.0.0.1"],
        limit=5,
        period=60,
        block_time=120,
    )


@pytest.mark.asyncio
async def test_rate_limit_middleware_skips_rate_limit_when_extractor_returns_no_keys() -> (
    None
):
    key_extractor = AsyncMock(return_value=[])
    use_case = AsyncMock()
    middleware = RateLimitMiddleware(
        FastAPI(),
        use_case,
        endpoint_configs={
            "/limited": EndpointConfig(
                limit=5,
                period=60,
                block_time=120,
                key_extractor=key_extractor,
            )
        },
    )
    request = _make_request(path="/limited")
    response = Response(status_code=200)
    call_next = AsyncMock(return_value=response)

    result = await middleware.dispatch(request, call_next)

    assert result is response
    use_case.allow_request.assert_not_awaited()
    call_next.assert_awaited_once_with(request)


@pytest.mark.asyncio
async def test_rate_limit_middleware_returns_429_for_blocked_request() -> None:
    key_extractor = AsyncMock(return_value=["user", "1"])
    use_case = AsyncMock()
    use_case.allow_request.return_value = (False, 33)
    middleware = RateLimitMiddleware(
        FastAPI(),
        use_case,
        endpoint_configs={
            "/limited": EndpointConfig(
                limit=5,
                period=60,
                block_time=120,
                key_extractor=key_extractor,
            )
        },
    )
    request = _make_request(path="/limited")
    call_next = AsyncMock()

    result = await middleware.dispatch(request, call_next)

    assert result.status_code == 429
    assert json.loads(result.body.decode()) == {
        "detail": "Too Many Requests. Please try again in 33 seconds",
        "block_time": 33,
    }
    call_next.assert_not_awaited()


@pytest.mark.asyncio
async def test_extract_ip_prefers_forwarded_header() -> None:
    request = _make_request(
        headers=[(b"x-forwarded-for", b"203.0.113.1, 10.0.0.1")],
        client_host="127.0.0.1",
    )

    assert await extract_ip(request) == ["ip", "203.0.113.1"]


@pytest.mark.asyncio
async def test_extract_ip_falls_back_to_request_client() -> None:
    request = _make_request(client_host="192.168.1.10")

    assert await extract_ip(request) == ["ip", "192.168.1.10"]
