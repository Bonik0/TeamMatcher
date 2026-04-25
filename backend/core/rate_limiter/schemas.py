from pydantic import BaseModel, PositiveInt
from typing import Awaitable, Callable
from fastapi import Request


class EndpointConfig(BaseModel):
    limit: PositiveInt
    period: PositiveInt
    block_time: PositiveInt
    key_extractor: Callable[[Request], Awaitable[list[str]]] | None
