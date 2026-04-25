from typing import Callable, Awaitable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
    Response,
)
from core.rate_limiter.use_case import RateLimitUseCase
from core.rate_limiter.utils import extract_ip
from core.rate_limiter.schemas import EndpointConfig


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        rate_limit_use_case: RateLimitUseCase,
        endpoint_configs: dict[str, EndpointConfig],
        default_key_extractor: Callable[[Request], Awaitable[list[str]]] | None = None,
    ) -> None:
        super().__init__(app)
        self.rate_limit_use_case = rate_limit_use_case
        self.default_key_extractor = default_key_extractor or extract_ip
        self.endpoint_configs = endpoint_configs

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        endpoint_path = request.url.path
        config = self.endpoint_configs.get(endpoint_path)

        if config is None:
            return await call_next(request)

        key_extractor = (
            config.key_extractor
            if config.key_extractor is not None
            else self.default_key_extractor
        )

        keys = await key_extractor(request)
        if not keys:
            return await call_next(request)

        allowed, block_ttl = await self.rate_limit_use_case.allow_request(
            keys=keys,
            limit=config.limit,
            period=config.period,
            block_time=config.block_time,
        )
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Too Many Requests. Please try again in {block_ttl} seconds",
                    "block_time": block_ttl,
                },
            )

        return await call_next(request)
