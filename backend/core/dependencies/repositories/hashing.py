from core.repositories.hashing import BcryptHashing


def get_hasing_repository() -> BcryptHashing:
    return BcryptHashing()
