from core.repositories.competence import SQLAlchemyCompetenceRepository


def get_competence_repository() -> SQLAlchemyCompetenceRepository:
    return SQLAlchemyCompetenceRepository()
