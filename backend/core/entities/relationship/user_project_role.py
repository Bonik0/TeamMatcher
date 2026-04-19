from core.entities.base.user_project_role import UserProjectRole
from core.entities.relationship.user import UserWithCompetences


class UserProjectRoleWithUserCompetences(UserProjectRole):
    user: UserWithCompetences
