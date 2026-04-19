from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy import Select, text
from sqlalchemy.dialects import postgresql


async def explain(session: AsyncSession, stmt: Select) -> None:
    query_str = stmt.compile(
        dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
    )
    result = await session.execute(text(f"EXPLAIN ANALYZE {query_str}"))

    for row in result:
        logging.info(row[0])
