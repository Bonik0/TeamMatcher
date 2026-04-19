from core.entities import ProjectRoleCompetence, UserCompetence, UserCompetenceLevelType
from decimal import Decimal
from app.match.utils.interfaces import ICompetenceSimilarityUtils


class CompetenceSimilarityUtils(ICompetenceSimilarityUtils):
    
    def __init__(
        self, 
        quantize: str, 
        user_competence_level_values: dict[UserCompetenceLevelType, Decimal]
    ) -> None:
        self.quantize = Decimal(quantize)
        self.user_competence_level_values = user_competence_level_values

    
    def convert_level(self, level: UserCompetenceLevelType) -> Decimal:
        return (
            self.user_competence_level_values
            .get(level, Decimal())
            .quantize(self.quantize)
        )
        
        
    def convert_importance(self, importance: int, importance_sum: int) -> Decimal:
        return (
            Decimal(importance) / Decimal(importance_sum)
        ).quantize(self.quantize)
    
    
    def get_importance_sum(self, project_competences: list[ProjectRoleCompetence]) -> int:
        return sum(
            (
                project_competence.importance
                for project_competence in project_competences
            )
        )
    
    
    def dot_competence(
        self, 
        importance: int, 
        level: UserCompetenceLevelType,
        importance_sum: int
    ) -> Decimal:
        return self.convert_importance(importance, importance_sum) * self.convert_level(level)


    def execute(
        self, 
        project_competences: list[ProjectRoleCompetence],
        user_competences: list[UserCompetence]
    ) -> Decimal:
        importance_sum = self.get_importance_sum(project_competences)
        if importance_sum == 0:
            return Decimal()
        
        competence_id_to_level = {
            user_competence.competence_id: user_competence.level
            for user_competence in user_competences
        }
        
        return sum(
            (
                self.dot_competence(
                    project_competence.importance, 
                    competence_id_to_level[project_competence.competence_id],
                    importance_sum
                )
                if project_competence.competence_id in competence_id_to_level else Decimal()
                for project_competence in project_competences
            )
        ).quantize(self.quantize)
        
        