from fastapi import FastAPI
from core.dependencies.CORS import set_default_cors_policy
import logging
from app.organizer.router import router as organizer_router
import os


app = FastAPI(
    root_path="/api/project",
)

set_default_cors_policy(app)

LOG_LEVEL = logging.INFO if (os.getenv("NT") != "TRUE") else logging.DEBUG

logging.basicConfig(
    level=LOG_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


set_default_cors_policy(app)

app.include_router(organizer_router)
