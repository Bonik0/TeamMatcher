from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_plan_format_teams_utils_create_schedules_celery_and_stores_task_id() -> (
    None
):
    from project_service.app.organizer.utils import PlanFormatTeamsUtils

    redis = AsyncMock()
    utils = PlanFormatTeamsUtils(redis)
    start = datetime.now() + timedelta(hours=2)

    with patch("project_service.app.organizer.utils.celery_match_task") as task_mock:
        task_mock.apply_async = MagicMock()
        await utils.create("42", start)

    task_mock.apply_async.assert_called_once()
    call_kw = task_mock.apply_async.call_args[1]
    assert call_kw["args"] == ["42"]
    assert "task_id" in call_kw
    redis.set.assert_awaited_once()
    key, stored_id = redis.set.await_args[0]
    assert key == "team_format:42"
    assert stored_id == call_kw["task_id"]


@pytest.mark.asyncio
async def test_plan_format_teams_utils_cancel_revokes_task_from_redis() -> None:
    from project_service.app.organizer.utils import PlanFormatTeamsUtils

    redis = AsyncMock()
    redis.get.return_value = b"task-uuid-123"
    utils = PlanFormatTeamsUtils(redis)

    with patch("project_service.app.organizer.utils.app") as celery_app:
        await utils.cancel(7)

    redis.get.assert_awaited_once_with("team_format:7")
    celery_app.control.revoke.assert_called_once_with(
        "task-uuid-123", terminate=True, signal="SIGKILL"
    )


@pytest.mark.asyncio
async def test_plan_format_teams_utils_update_cancels_then_creates() -> None:
    from project_service.app.organizer.utils import PlanFormatTeamsUtils

    redis = AsyncMock()
    redis.get.return_value = b"old-task"
    utils = PlanFormatTeamsUtils(redis)
    start = datetime.now() + timedelta(hours=1)

    with (
        patch.object(utils, "cancel", new_callable=AsyncMock) as cancel_mock,
        patch.object(utils, "create", new_callable=AsyncMock) as create_mock,
    ):
        await utils.update(3, start)

    cancel_mock.assert_awaited_once_with(3)
    create_mock.assert_awaited_once_with(3, start)
