from core.entities.base.user import User
from core.entities.base.user_competence import UserCompetence
from core.entities.base.user_project_role import UserProjectRole


class UserWithCompetences(User):
    competences: list[UserCompetence]


class UserWithForms(User):
    forms: list[UserProjectRole]


class UserWithFormsAndCompetences(UserWithCompetences, UserWithForms):
    pass
