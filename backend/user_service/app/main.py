from fastapi import FastAPI
from core.dependencies.CORS import set_default_cors_policy
import logging
from app.user_competence.router import router as user_competence_router
from app.user_role.router import router as user_role_router
from app.user_team.router import router as team_router

app = FastAPI(
    root_path="/api/user",
)

set_default_cors_policy(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


set_default_cors_policy(app)

app.include_router(user_competence_router)
app.include_router(user_role_router)
app.include_router(team_router)
