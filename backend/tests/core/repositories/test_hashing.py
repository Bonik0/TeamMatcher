from hashlib import sha256

from core.repositories.hashing import ShaHashing


def test_hash_password_returns_sha256_hexdigest() -> None:
    repository = ShaHashing()

    assert repository.hash_password("secret") == sha256(b"secret").hexdigest()


def test_verify_password_returns_true_for_matching_hash() -> None:
    repository = ShaHashing()
    hashed_password = repository.hash_password("secret")

    assert repository.verify_password("secret", hashed_password) is True


def test_verify_password_returns_false_for_non_matching_hash() -> None:
    repository = ShaHashing()

    assert repository.verify_password("secret", "wrong-hash") is False
