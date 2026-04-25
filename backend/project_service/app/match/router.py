from celery import Celery
from asgiref.sync import async_to_sync
from core.models.redis.config import get_redis_url
import logging

app = Celery("tasks", broker=get_redis_url(), backend=get_redis_url())


@app.task(bind=True, max_retries=3)
def celery_match_task(self, project_id: int) -> None:
    from app.match.dependencies.utils import (
        get_competence_similarity_utils,
        get_match_utils,
        get_user_project_role_similarity_utils,
    )
    from app.match.dependencies.use_cases import get_match_use_case
    from core.dependencies.repositories.project import get_project_repository
    from core.dependencies.repositories.user import get_user_repository
    from core.dependencies.repositories.team import get_team_repository

    from core.models.postgres import async_session_maker

    logger = logging.getLogger(__name__)
    session = async_session_maker()

    competence_utils = get_competence_similarity_utils()
    role_utils = get_user_project_role_similarity_utils()
    match_utils = get_match_utils(competence_utils, role_utils)

    project_repository = get_project_repository()
    user_repository = get_user_repository()
    team_repository = get_team_repository()

    use_case = get_match_use_case(
        project_repository, user_repository, team_repository, match_utils, logger
    )

    try:
        async_to_sync(use_case.execute)(session, project_id)
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
