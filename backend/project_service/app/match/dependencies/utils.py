from app.match.utils.competence_similarity import CompetenceSimilarityUtils
from app.match.utils.user_project_role_similarity import UserProjectRoleSimilarityUtils
from app.match.utils.match_utils import MatchUtils
from app.match.utils.interfaces import (
    IUserProjectRoleSimilarityUtils,
    ICompetenceSimilarityUtils,
)
from core.entities import UserCompetenceLevelType
from decimal import Decimal


def get_competence_similarity_utils() -> CompetenceSimilarityUtils:
    from app.match.config import match_settings

    return CompetenceSimilarityUtils(
        quantize=match_settings.QUANTIZE,
        user_competence_level_values={
            UserCompetenceLevelType.LOW: Decimal(match_settings.LOW_LEVEL_VALUE),
            UserCompetenceLevelType.MIDDLE: Decimal(match_settings.MIDDLE_LEVEL_VALUE),
            UserCompetenceLevelType.HIGH: Decimal(match_settings.HIGH_LEVEL_VALUE),
        },
    )


def get_user_project_role_similarity_utils() -> UserProjectRoleSimilarityUtils:
    from app.match.config import match_settings

    return UserProjectRoleSimilarityUtils(
        quantize=match_settings.QUANTIZE,
        desired_role_coeff=match_settings.DESIRDED_ROLE_COEFF,
        role_priority_bonus_coeff=match_settings.ROLE_PRIORITY_BONUS_COEFF,
    )


def get_match_utils(
    competence_utils: ICompetenceSimilarityUtils,
    role_utils: IUserProjectRoleSimilarityUtils,
) -> MatchUtils:
    return MatchUtils(competence_utils=competence_utils, similarity_utils=role_utils)
