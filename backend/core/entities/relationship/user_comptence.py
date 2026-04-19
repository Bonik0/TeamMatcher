from core.entities.base.competence import Competence
from core.entities.base.user_competence import UserCompetence


class UserCompetenceWithCompetence(UserCompetence):
    competence: Competence
