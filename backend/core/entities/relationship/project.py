from core.entities.relationship.project_role import (
    ProjectRoleWithRoleAndProjectRoleCompetences,
    ProjectRoleWithRole,
    ProjectRoleWithRoleAndForms,
    ProjectRoleWithCompetencesAndUserCompetences,
)
from core.entities.base.project import Project
from core.entities.relationship.team import TeamWithMembers


class ProjectWithRoles(Project):
    roles: list[ProjectRoleWithRole]


class ProjectWithRolesAndCompetences(Project):
    roles: list[ProjectRoleWithRoleAndProjectRoleCompetences]


class ProjectWithRolesAndForms(Project):
    roles: list[ProjectRoleWithRoleAndForms]


class ProjectWithCompetencesAndUserCompetences(Project):
    roles: list[ProjectRoleWithCompetencesAndUserCompetences]


class ProjectWithRolesAndTeams(ProjectWithRoles):
    teams: list[TeamWithMembers]
