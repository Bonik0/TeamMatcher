import bcrypt
from core.interfaces.repositories.hashing import IHashingRepository


class BcryptHashing(IHashingRepository):
    def __init__(self, salt: bytes | None = None) -> None:
        self.salt = salt

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), self.salt or bcrypt.gensalt()).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
