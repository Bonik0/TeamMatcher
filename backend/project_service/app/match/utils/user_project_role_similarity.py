import sys
from core.entities import UserWithFormsAndCompetences, ProjectRoleWithRoleAndProjectRoleCompetences, UserProjectRole, UserCompetenceLevelType
from decimal import Decimal
from app.match.utils.interfaces import IUserProjectRoleSimilarityUtils, ICompetenceSimilarityUtils







class UserProjectRoleSimilarityUtils(IUserProjectRoleSimilarityUtils):
    
    def __init__(
        self, 
        quantize: str, 
        desired_role_coeff: str = "1.0",
        role_priority_bonus_coeff: str = "1.0"
    ) -> None:
        self.quantize = Decimal(quantize)
        self.desired_role_coeff = Decimal(desired_role_coeff)
        self.role_priority_bonus_coeff = Decimal(role_priority_bonus_coeff)
        
    
    def get_role_priority_bonus(self, priority: int, max_priority: int) -> Decimal:
        return (
            self.role_priority_bonus_coeff * ( 
                Decimal(max_priority - (priority - 1)) / max_priority
            )
        ).quantize(self.quantize)
        
    def get_role_priority(
        self, 
        user_forms: list[UserProjectRole],
        project_role_id: int
    ) -> int | None:
        return next(
            (
                user_role.priority
                for user_role in user_forms
                if user_role.project_role_id == project_role_id
            ), None
        )
    
    
    def execute(
        self, 
        competence_match: Decimal,
        user_roles: list[UserProjectRole],
        project_role_id: int
    ) -> Decimal:
        role_priority = self.get_role_priority(user_roles, project_role_id)
        max_priority = len(user_roles)
        if role_priority is None:
            return (
                competence_match * self.desired_role_coeff
            ).quantize(self.quantize)
        return (
            self.desired_role_coeff + 
            competence_match + 
            self.get_role_priority_bonus(role_priority, max_priority)
        ).quantize(self.quantize)
        
        
