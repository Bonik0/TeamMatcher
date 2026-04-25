from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import literal, select

from core.utils.postgres import explain


@pytest.mark.asyncio
async def test_explain_executes_explain_analyze_and_logs_plan_rows() -> None:
    session = AsyncMock()
    session.execute.return_value = [("Seq Scan on users",), ("Planning Time: 0.1 ms",)]
    stmt = select(literal(1))

    with patch("core.utils.postgres.logging.info") as info_mock:
        await explain(session, stmt)

    executed_query = session.execute.await_args.args[0]
    assert "EXPLAIN ANALYZE" in str(executed_query)
    assert "SELECT 1 AS anon_1" in str(executed_query)
    assert [call.args[0] for call in info_mock.call_args_list] == [
        "Seq Scan on users",
        "Planning Time: 0.1 ms",
    ]
