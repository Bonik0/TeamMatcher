from app.user_competence.use_cases.add_or_update_user_competence_use_case import (
    AddOrUpdateUserCompetencesUseCase,
)
from app.user_competence.use_cases.remove_user_competence_use_case import (
    RemoveUserCompetencesUseCase,
)
from app.user_competence.use_cases.find_user_competence_use_case import (
    FindUserCompetencesUseCase,
)
from fastapi import Depends
from core.interfaces.repositories.competence import ICompetenceRepository
from core.dependencies.repositories.competence import get_competence_repository


def get_add_or_update_use_case(
    competence_repository: ICompetenceRepository = Depends(get_competence_repository),
) -> AddOrUpdateUserCompetencesUseCase:
    return AddOrUpdateUserCompetencesUseCase(competence_repository)


def get_remove_use_case(
    competence_repository: ICompetenceRepository = Depends(get_competence_repository),
) -> RemoveUserCompetencesUseCase:
    return RemoveUserCompetencesUseCase(competence_repository)


def get_find_use_case(
    competence_repository: ICompetenceRepository = Depends(get_competence_repository),
) -> FindUserCompetencesUseCase:
    return FindUserCompetencesUseCase(competence_repository)
