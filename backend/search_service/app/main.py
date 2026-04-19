from fastapi import FastAPI
from core.dependencies.CORS import set_default_cors_policy
import logging
from app.search.router import router as search_router

app = FastAPI(
    root_path="/api",
)

set_default_cors_policy(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


set_default_cors_policy(app)

app.include_router(search_router)
