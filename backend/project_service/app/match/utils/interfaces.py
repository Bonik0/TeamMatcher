from core.entities import ProjectRoleCompetence, UserCompetence, UserProjectRole, UserWithFormsAndCompetences, ProjectRoleWithCompetences, UserProjectScore
from decimal import Decimal
from typing import Protocol

class ICompetenceSimilarityUtils(Protocol):
    
    def execute(
        self, 
        project_competences: list[ProjectRoleCompetence],
        user_competences: list[UserCompetence]
    ) -> Decimal:
        pass
    
    
class IUserProjectRoleSimilarityUtils(Protocol):
    
    def execute(
        self, 
        competence_match: Decimal,
        user_roles: list[UserProjectRole],
        project_role_id: int
    ) -> Decimal:
        pass
    
    
class IMatchUtils(Protocol):
    
    def execute(
        self, 
        users: list[UserWithFormsAndCompetences],
        project_roles: list[ProjectRoleWithCompetences], 
    ) -> list[list[UserProjectScore]]:
        pass