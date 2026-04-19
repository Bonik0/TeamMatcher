from typing import Protocol


class IHashingRepository(Protocol):
    def hash_password(self, password: str) -> str:
        pass

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
