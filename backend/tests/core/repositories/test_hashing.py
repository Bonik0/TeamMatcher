from bcrypt import hashpw, gensalt
from core.repositories.hashing import BcryptHashing


def test_hash_password_returns_bcrypt_hexdigest() -> None:
    salt = gensalt()
    repository = BcryptHashing(salt)
    assert (
        repository.hash_password("secret") == hashpw("secret".encode(), salt).decode()
    )


def test_verify_password_returns_true_for_matching_hash() -> None:
    repository = BcryptHashing()
    hashed_password = repository.hash_password("secret")

    assert repository.verify_password("secret", hashed_password) is True


def test_verify_password_returns_false_for_non_matching_hash() -> None:
    repository = BcryptHashing()
    hashed_password = repository.hash_password("wrong-hash")
    assert repository.verify_password("secret", hashed_password) is False
