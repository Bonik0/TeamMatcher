from core.repositories.project import SQLAlchemyProjectRepository


def get_project_repository() -> SQLAlchemyProjectRepository:
    return SQLAlchemyProjectRepository()
