from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.jwttoken.router import router as jwttoken_router
from app.user_verify.router import router as user_verify_router
from core.dependencies.CORS import set_default_cors_policy
from core.rate_limiter import RateLimitMiddleware, EndpointConfig
from core.dependencies.rate_limiter import get_rate_limiter_use_case
import logging
from app.auth.utils import login_key_executor


app = FastAPI(
    root_path="/api/auth",
)

set_default_cors_policy(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

rate_limit_logger = logging.getLogger("Rate Limit")

endpoint_configs = {
    "/api/auth/login": EndpointConfig(
        limit=5, period=180, block_time=60, key_extractor=login_key_executor
    ),
}


set_default_cors_policy(app)
app.add_middleware(
    RateLimitMiddleware,
    rate_limit_use_case=get_rate_limiter_use_case(rate_limit_logger),
    endpoint_configs=endpoint_configs,
)

app.include_router(auth_router)
app.include_router(jwttoken_router)
app.include_router(user_verify_router)
