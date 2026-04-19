import sys
sys.path.append("/home/bonik/giploma/backend")
sys.path.append("/home/bonik/giploma/backend/project_service")
import pytest
from decimal import Decimal
from core.entities import UserCompetenceLevelType, ProjectRoleCompetence, UserCompetence
from project_service.app.match.utils.competence_similarity import CompetenceSimilarityUtils

@pytest.fixture
def utils():
    return CompetenceSimilarityUtils(
        quantize="0.01", 
        user_competence_level_values={
            UserCompetenceLevelType.LOW: Decimal("0.5"),
            UserCompetenceLevelType.MIDDLE: Decimal("0.75"),
            UserCompetenceLevelType.HIGH: Decimal("1.0")
        }
    )

class TestConvertLevel:
    def test_convert_level_low(self, utils):
        assert utils.convert_level(UserCompetenceLevelType.LOW) == Decimal("0.5")
    
    def test_convert_level_middle(self, utils):
        assert utils.convert_level(UserCompetenceLevelType.MIDDLE) == Decimal("0.75")
    
    def test_convert_level_high(self, utils):
        assert utils.convert_level(UserCompetenceLevelType.HIGH) == Decimal("1.0")
    
    def test_convert_level_unknown(self, utils):
        assert utils.convert_level(999) == Decimal("0.0")  

class TestConvertImportance:
    def test_convert_importance(self, utils):
        assert utils.convert_importance(importance=2, importance_sum=10) == Decimal("0.2")
        assert utils.convert_importance(5, 5) == Decimal("1.0")
        assert utils.convert_importance(0, 5) == Decimal("0.0")
    
    def test_convert_importance_rounding(self, utils):
        result = utils.convert_importance(1, 3)
        assert result == Decimal("0.33") 

class TestGetImportanceSum:
    def test_empty_list(self, utils):
        assert utils.get_importance_sum([]) == 0
    
    def test_single_competence(self, utils):
        comp = ProjectRoleCompetence(project_role_id=1, competence_id=1, importance=5)
        assert utils.get_importance_sum([comp]) == 5
    
    def test_multiple_competences(self, utils):
        comps = [
            ProjectRoleCompetence(project_role_id=1, competence_id=1, importance=3),
            ProjectRoleCompetence(project_role_id=1, competence_id=2, importance=7),
        ]
        assert utils.get_importance_sum(comps) == 10

class TestDotCompetence:
    def test_dot_competence(self, utils):
        importance_sum = 10
        result = utils.dot_competence(importance=4, level=UserCompetenceLevelType.HIGH, importance_sum=importance_sum)
        assert result == Decimal("0.4")
    
    def test_dot_competence_low_level(self, utils):
        result = utils.dot_competence(importance=6, level=UserCompetenceLevelType.LOW, importance_sum=12)
        assert result == Decimal("0.25")

class TestExecute:
    def test_perfect_match(self, utils):
        project_comps = [
            ProjectRoleCompetence(project_role_id=1, competence_id=1, importance=2),
            ProjectRoleCompetence(project_role_id=1, competence_id=2, importance=3),
        ]
        user_comps = [
            UserCompetence(user_id=1, competence_id=1, level=UserCompetenceLevelType.HIGH),
            UserCompetence(user_id=1, competence_id=2, level=UserCompetenceLevelType.HIGH),
        ]
        score = utils.execute(project_comps, user_comps)
        assert score == Decimal("1.0")
    
    def test_partial_match(self, utils):
        project_comps = [
            ProjectRoleCompetence(project_role_id=1, competence_id=1, importance=4),
            ProjectRoleCompetence(project_role_id=1, competence_id=2, importance=6),
        ]
        user_comps = [
            UserCompetence(user_id=1, competence_id=1, level=UserCompetenceLevelType.HIGH),
            UserCompetence(user_id=1, competence_id=2, level=UserCompetenceLevelType.LOW),
        ]
        score = utils.execute(project_comps, user_comps)
        assert score == Decimal("0.7")
    
    def test_missing_competence(self, utils):
        project_comps = [
            ProjectRoleCompetence(project_role_id=1, competence_id=1, importance=5),
            ProjectRoleCompetence(project_role_id=1, competence_id=2, importance=5),
        ]
        user_comps = [
            UserCompetence(user_id=1, competence_id=1, level=UserCompetenceLevelType.HIGH),
        ]
        score = utils.execute(project_comps, user_comps)
        assert score == Decimal("0.5")
    
    def test_all_missing(self, utils):
        project_comps = [
            ProjectRoleCompetence(project_role_id=1, competence_id=1, importance=7),
            ProjectRoleCompetence(project_role_id=1, competence_id=2, importance=3),
        ]
        user_comps = []  
        score = utils.execute(project_comps, user_comps)
        assert score == Decimal("0.0")
    
    def test_empty_project_competences(self, utils):
        score = utils.execute([], [])
        assert score == Decimal("0.0")
    