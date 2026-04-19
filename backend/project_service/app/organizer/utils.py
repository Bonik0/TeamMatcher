from datetime import datetime
from app.match.router import celery_match_task, app
from redis.asyncio import Redis
import uuid


class PlanFormatTeamsUtils:
    def __init__(self, client: Redis) -> None:
        self.client = client

    def _get_team_format_key(self, project_id: int) -> str:
        return f"team_format:{project_id}"

    async def create(self, project_id: str, start_time: datetime) -> None:

        new_task_id = str(uuid.uuid4())
        countdown = start_time - datetime.now()

        celery_match_task.apply_async(
            args=[project_id],
            countdown=int(countdown.total_seconds()),
            task_id=new_task_id,
        )
        await self.client.set(self._get_team_format_key(project_id), new_task_id)

    async def cancel(self, project_id: int) -> None:
        task_id = await self.client.get(self._get_team_format_key(project_id))
        app.control.revoke(task_id.decode(), terminate=True, signal="SIGKILL")

    async def update(self, project_id: int, start_time: datetime) -> None:
        await self.cancel(project_id)
        await self.create(project_id, start_time)
