from hashlib import sha256
from core.interfaces.repositories.hashing import IHashingRepository


class ShaHashing(IHashingRepository):
    def hash_password(self, password: str) -> str:
        return sha256(password.encode("utf-8")).hexdigest()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.hash_password(plain_password) == hashed_password
