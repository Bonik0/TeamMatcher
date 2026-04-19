from core.entities.base.project_role import ProjectRole
from core.entities.base.role import Role
from core.entities.base.project_role_competence import ProjectRoleCompetence
from core.entities.relationship.project_role_competence import (
    ProjectRoleCompetenceWithCompetence,
)
from core.entities.base.user_project_role import UserProjectRole
from core.entities.relationship.user_project_role import UserProjectRoleWithUserCompetences

class ProjectRoleWithRole(ProjectRole):
    role: Role


class ProjectRoleWithRoleAndProjectRoleCompetences(ProjectRoleWithRole):
    competences: list[ProjectRoleCompetenceWithCompetence]


class ProjectRoleWithRoleAndForms(ProjectRoleWithRole):
    forms: list[UserProjectRole]
    
    
class ProjectRoleWithCompetencesAndUserCompetences(ProjectRole):
    competences: list[ProjectRoleCompetence]
    forms: list[UserProjectRoleWithUserCompetences]
    
    
class ProjectRoleWithCompetences(ProjectRole):
    competences: list[ProjectRoleCompetence]
