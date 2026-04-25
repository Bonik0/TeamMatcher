from core.repositories.user import SQLAlchemyUserRepository


def get_user_repository() -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository()
