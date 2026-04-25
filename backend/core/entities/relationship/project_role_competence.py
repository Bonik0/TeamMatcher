from core.entities.base.project_role_competence import ProjectRoleCompetence
from core.entities.base.competence import Competence


class ProjectRoleCompetenceWithCompetence(ProjectRoleCompetence):
    competence: Competence
