from core.repositories.role import SQLAlchemyRoleRepository


def get_role_repository() -> SQLAlchemyRoleRepository:
    return SQLAlchemyRoleRepository()
