import pytest
from decimal import Decimal
from core.entities import (
    UserProjectRole,
)
from project_service.app.match.utils.user_project_role_similarity import (
    UserProjectRoleSimilarityUtils,
)


@pytest.fixture
def utils():
    return UserProjectRoleSimilarityUtils(
        quantize="0.01", desired_role_coeff="1.0", role_priority_bonus_coeff="1.0"
    )


@pytest.fixture
def sample_user_forms():
    return [
        UserProjectRole(user_id=1, project_role_id=101, priority=1),
        UserProjectRole(user_id=1, project_role_id=102, priority=2),
        UserProjectRole(user_id=1, project_role_id=103, priority=3),
    ]


class TestGetRolePriorityBonus:
    def test_priority_first(self, utils):
        bonus = utils.get_role_priority_bonus(priority=1, max_priority=3)
        assert bonus == Decimal("1.00")

    def test_priority_second(self, utils):
        bonus = utils.get_role_priority_bonus(priority=2, max_priority=3)
        assert bonus == Decimal("0.67")

    def test_priority_last(self, utils):
        bonus = utils.get_role_priority_bonus(priority=3, max_priority=3)
        assert bonus == Decimal("0.33")

    def test_max_priority_one(self, utils):
        bonus = utils.get_role_priority_bonus(priority=1, max_priority=1)
        assert bonus == Decimal("1.00")

    def test_with_coeff(self):
        utils_custom = UserProjectRoleSimilarityUtils(
            quantize="0.01", desired_role_coeff="1.0", role_priority_bonus_coeff="0.5"
        )
        bonus = utils_custom.get_role_priority_bonus(priority=1, max_priority=3)
        assert bonus == Decimal("0.50")


class TestGetRolePriority:
    def test_found(self, utils, sample_user_forms):
        priority = utils.get_role_priority(sample_user_forms, 102)
        assert priority == 2

    def test_not_found(self, utils, sample_user_forms):
        priority = utils.get_role_priority(sample_user_forms, 999)
        assert priority is None


class TestExecute:
    def test_undesired_role(self, utils):
        sample_user_forms = [
            UserProjectRole(user_id=1, project_role_id=200, priority=1)
        ]
        score = utils.execute(Decimal("0.85"), sample_user_forms, 101)
        assert score == Decimal("0.85")

    def test_desired_role_first_priority(self, utils, sample_user_forms):
        score = utils.execute(Decimal("0.70"), sample_user_forms, 101)
        assert score == Decimal("2.70")

    def test_desired_role_second_priority(self, utils, sample_user_forms):

        score = utils.execute(Decimal("0.50"), sample_user_forms, 102)
        assert score == Decimal("2.17")

    def test_desired_role_third_priority(self, utils, sample_user_forms):
        score = utils.execute(Decimal("0.90"), sample_user_forms, 103)
        # bonus = (3 - (3-1))/3 = (3-2)/3 = 1/3 ≈ 0.33
        # 1.0 + 0.90 + 0.33 = 2.23
        assert score == Decimal("2.23")

    def test_max_priority_one(self, utils):
        forms = [UserProjectRole(user_id=1, project_role_id=101, priority=1)]
        score = utils.execute(Decimal("0.40"), forms, 101)
        # bonus = (1 - (1-1))/1 = 1.0
        # 1.0 + 0.40 + 1.0 = 2.40
        assert score == Decimal("2.40")

    def test_custom_coeffs(self):
        utils_custom = UserProjectRoleSimilarityUtils(
            quantize="0.001", desired_role_coeff="2.0", role_priority_bonus_coeff="0.3"
        )

        user_forms = [UserProjectRole(user_id=1, project_role_id=101, priority=1)]
        score = utils_custom.execute(Decimal("0.60"), user_forms, 101)
        # desired_coeff=2.0 + competence_match=0.60 + bonus=0.3*1=0.3 => 2.9
        assert score == Decimal("2.900")
        score2 = utils_custom.execute(Decimal("0.60"), [], 101)
        # competence_match * desired_role_coeff = 0.60 * 2.0 = 1.2
        assert score2 == Decimal("1.200")

    def test_quantization(self):
        utils_quant = UserProjectRoleSimilarityUtils(
            quantize="0.1", desired_role_coeff="1.0", role_priority_bonus_coeff="1.0"
        )
        user_forms = [UserProjectRole(user_id=1, project_role_id=101, priority=1)]
        score = utils_quant.execute(Decimal("0.33333"), user_forms, 101)
        # 1.0 + 0.33333 + 1.0 = 2.33333 -> quantize 0.1 => 2.3
        assert score == Decimal("2.3")


class TestEdgeCases:
    def test_zero_priority_bonus_coeff(self):
        utils_zero = UserProjectRoleSimilarityUtils(
            quantize="0.01", desired_role_coeff="1.0", role_priority_bonus_coeff="0"
        )

        user_forms = [UserProjectRole(user_id=1, project_role_id=101, priority=1)]
        score = utils_zero.execute(Decimal("0.80"), user_forms, 101)
        # desired_coeff + competence_match + 0 = 1.0 + 0.80 = 1.80
        assert score == Decimal("1.80")

    def test_zero_desired_coeff(self):
        utils_zero = UserProjectRoleSimilarityUtils(
            quantize="0.01", desired_role_coeff="0", role_priority_bonus_coeff="1.0"
        )
        user_forms = [UserProjectRole(user_id=1, project_role_id=101, priority=1)]
        score = utils_zero.execute(Decimal("0.50"), user_forms, 101)
        # desired_coeff=0 + competence_match + bonus = 0 + 0.50 + 1.0 = 1.50
        assert score == Decimal("1.50")
        score_undesired = utils_zero.execute(Decimal("0.50"), [], 101)
        assert score_undesired == Decimal("0.00")

    def test_no_competences_match(self, utils, sample_user_forms):
        score = utils.execute(Decimal("0.00"), sample_user_forms, 101)
        # 1.0 + 0.0 + 1.0 = 2.0
        assert score == Decimal("2.00")
