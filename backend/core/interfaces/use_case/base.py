from typing import Protocol, Any


class IUseCase(Protocol):
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass
