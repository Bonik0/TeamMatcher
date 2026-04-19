from core.repositories.hashing import ShaHashing


def get_hasing_repository() -> ShaHashing:
    return ShaHashing()
