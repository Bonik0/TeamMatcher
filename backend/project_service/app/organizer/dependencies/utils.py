from app.organizer.utils import PlanFormatTeamsUtils
from redis.asyncio import Redis
from core.dependencies.redis import get_redis_client
from fastapi import Depends


def get_formating_teams_utils(client: Redis = Depends(get_redis_client)) -> PlanFormatTeamsUtils:
    return PlanFormatTeamsUtils(client)