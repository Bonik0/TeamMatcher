from fastapi import FastAPI
from app.email_verify.rounter import router as email_verify_router
from core.dependencies.CORS import set_default_cors_policy
from core.rate_limiter import RateLimitMiddleware, EndpointConfig
from core.dependencies.rate_limiter import get_rate_limiter_use_case
import logging
from app.email_verify.utils import email_verify_key_executor
from core.models.rabbitmq import rabbitmq_router

app = FastAPI(
    root_path="/api/email",
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

rate_limit_logger = logging.getLogger("Rate Limit")

endpoint_configs = {
    "/api/email/code/send": EndpointConfig(
        limit=1, period=180, block_time=60, key_extractor=email_verify_key_executor
    ),
}


set_default_cors_policy(app)
app.add_middleware(
    RateLimitMiddleware,
    rate_limit_use_case=get_rate_limiter_use_case(rate_limit_logger),
    endpoint_configs=endpoint_configs,
)


app.include_router(email_verify_router)
app.include_router(rabbitmq_router)
