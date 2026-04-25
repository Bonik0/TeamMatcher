import pytest
from decimal import Decimal
from unittest.mock import create_autospec

from project_service.app.match.utils.match_utils import MatchUtils
from project_service.app.match.utils.interfaces import (
    ICompetenceSimilarityUtils,
    IUserProjectRoleSimilarityUtils,
)
from core.entities import (
    UserProjectScore,
    UserWithFormsAndCompetences,
    ProjectRoleWithCompetences,
    UserProjectRole,
    UserCompetence,
    ProjectRoleCompetence,
    ProjectRole,
    UserCompetenceLevelType,
)
from copy import deepcopy


@pytest.fixture
def mock_competence_utils():
    return create_autospec(ICompetenceSimilarityUtils)


@pytest.fixture
def mock_similarity_utils():
    return create_autospec(IUserProjectRoleSimilarityUtils)


@pytest.fixture
def match_utils(mock_competence_utils, mock_similarity_utils):
    return MatchUtils(
        competence_utils=mock_competence_utils, similarity_utils=mock_similarity_utils
    )


@pytest.fixture
def sample_roles():
    return [
        ProjectRole(
            id=1, project_id=1, role_id=101, description=None, quantity_per_team=2
        ),
        ProjectRole(
            id=2, project_id=1, role_id=102, description=None, quantity_per_team=1
        ),
    ]


class TestComputeScores:
    def test_compute_scores_calls_utils_correctly(
        self, match_utils, mock_competence_utils, mock_similarity_utils
    ):
        user = UserWithFormsAndCompetences(
            id=1,
            email="a@a.com",
            first_name="Ivan",
            surname="Ivanov",
            patronymic=None,
            role="user",
            hash_password="hash",
            forms=[UserProjectRole(user_id=1, project_role_id=10, priority=1)],
            competences=[
                UserCompetence(
                    user_id=1, competence_id=5, level=UserCompetenceLevelType.HIGH
                )
            ],
        )
        role = ProjectRoleWithCompetences(
            id=10,
            project_id=100,
            role_id=200,
            description="test",
            quantity_per_team=1,
            competences=[
                ProjectRoleCompetence(project_role_id=10, competence_id=5, importance=8)
            ],
        )
        mock_competence_utils.execute.return_value = Decimal("0.75")
        mock_similarity_utils.execute.return_value = Decimal("1.85")

        result = match_utils.compute_scores([user], [role])

        assert len(result) == 1
        score_entry = result[0]
        assert score_entry.user_id == 1
        assert score_entry.project_role_id == 10
        assert score_entry.competence_match == Decimal("0.75")
        assert score_entry.role_score == Decimal("1.85")

        mock_competence_utils.execute.assert_called_once_with(
            project_competences=role.competences, user_competences=user.competences
        )
        mock_similarity_utils.execute.assert_called_once_with(
            competence_match=Decimal("0.75"), user_roles=user.forms, project_role_id=10
        )

    def test_compute_scores_multiple_users_and_roles(
        self, match_utils, mock_competence_utils, mock_similarity_utils
    ):
        users = [
            UserWithFormsAndCompetences(
                id=1,
                email="a@a.com",
                first_name="A",
                surname="A",
                patronymic=None,
                role="user",
                hash_password="h",
                forms=[],
                competences=[],
            ),
            UserWithFormsAndCompetences(
                id=2,
                email="b@b.com",
                first_name="B",
                surname="B",
                patronymic=None,
                role="user",
                hash_password="h",
                forms=[],
                competences=[],
            ),
        ]
        roles = [
            ProjectRoleWithCompetences(
                id=101,
                project_id=1,
                role_id=1,
                description="r1",
                quantity_per_team=1,
                competences=[],
            ),
            ProjectRoleWithCompetences(
                id=102,
                project_id=1,
                role_id=2,
                description="r2",
                quantity_per_team=1,
                competences=[],
            ),
        ]
        mock_competence_utils.execute.return_value = Decimal("0.5")
        mock_similarity_utils.execute.return_value = Decimal("1.2")

        result = match_utils.compute_scores(users, roles)

        assert len(result) == 4
        pairs = {(score.user_id, score.project_role_id) for score in result}
        expected_pairs = {(1, 101), (1, 102), (2, 101), (2, 102)}
        assert pairs == expected_pairs
        for score in result:
            assert score.competence_match == Decimal("0.5")
            assert score.role_score == Decimal("1.2")


class TestGetMaxTeamsNumber:
    def test_exact_division(self):
        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=10, description="d1", quantity_per_team=2
            ),
            ProjectRole(
                id=2, project_id=1, role_id=20, description="d2", quantity_per_team=1
            ),
        ]
        # sum = 3, users_count=6 -> 6/3=2
        utils = MatchUtils(None, None)  # моки не нужны
        assert utils.get_max_teams_number(roles, 6) == 2

    def test_ceil_division(self):
        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=10, description="d1", quantity_per_team=2
            ),
            ProjectRole(
                id=2, project_id=1, role_id=20, description="d2", quantity_per_team=1
            ),
        ]
        # sum=3, users_count=7 -> 7/3≈2.333 -> ceil=3
        utils = MatchUtils(None, None)
        assert utils.get_max_teams_number(roles, 7) == 3

    def test_one_user(self):
        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=10, description="d1", quantity_per_team=2
            )
        ]
        # sum=2, users_count=1 -> 0.5 -> ceil=1
        utils = MatchUtils(None, None)
        assert utils.get_max_teams_number(roles, 1) == 1

    def test_zero_users(self):
        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=10, description="d1", quantity_per_team=2
            )
        ]
        utils = MatchUtils(None, None)
        assert utils.get_max_teams_number(roles, 0) == 0


class TestGetUndalancedTeams:
    def test_adds_dummy_users_when_not_enough(self, match_utils, sample_roles):
        assignments = [
            UserProjectScore(
                user_id=1,
                project_role_id=1,
                competence_match=Decimal("0.9"),
                role_score=Decimal("10"),
            ),
            UserProjectScore(
                user_id=2,
                project_role_id=1,
                competence_match=Decimal("0.8"),
                role_score=Decimal("10"),
            ),
            UserProjectScore(
                user_id=3,
                project_role_id=2,
                competence_match=Decimal("0.7"),
                role_score=Decimal("10"),
            ),
        ]
        teams = match_utils.assign_unbalanced_teams(
            assignments, sample_roles, num_teams=2
        )

        total_users = sum(len(team) for team in teams)
        assert total_users == 6

        dummy_count = sum(
            1 for team in teams for u in team if u.user_id == match_utils.fake_user_id
        )
        assert dummy_count == 3

        real_ids = {
            u.user_id
            for team in teams
            for u in team
            if u.user_id != match_utils.fake_user_id
        }
        assert real_ids == {1, 2, 3}

    def test_truncates_excess_users_when_too_many(self, match_utils, sample_roles):
        assignments = [
            UserProjectScore(
                user_id=i,
                project_role_id=1,
                competence_match=Decimal(str(1 - i * 0.1)),
                role_score=Decimal("10"),
            )
            for i in range(1, 7)
        ] + [
            UserProjectScore(
                user_id=i + 10,
                project_role_id=2,
                competence_match=Decimal(str(1 - i * 0.1)),
                role_score=Decimal("10"),
            )
            for i in range(1, 5)
        ]
        teams = match_utils.assign_unbalanced_teams(
            assignments, sample_roles, num_teams=2
        )

        total_users = sum(len(team) for team in teams)
        assert total_users == 6  # 4+2

        role1_values = [
            u.competence_match for team in teams for u in team if u.project_role_id == 1
        ]
        role1_values_sorted = sorted(role1_values, reverse=True)
        assert role1_values_sorted == [
            Decimal("0.9"),
            Decimal("0.8"),
            Decimal("0.7"),
            Decimal("0.6"),
        ]

        role2_values = [
            u.competence_match for team in teams for u in team if u.project_role_id == 2
        ]
        assert sorted(role2_values, reverse=True) == [Decimal("0.9"), Decimal("0.8")]

    def test_distribution_blockwise(self, match_utils, sample_roles):

        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=101, description=None, quantity_per_team=2
            ),
            ProjectRole(
                id=2, project_id=1, role_id=102, description=None, quantity_per_team=1
            ),
        ]
        role1_users = [
            UserProjectScore(
                user_id=i,
                project_role_id=1,
                competence_match=Decimal(str(10 - i)),
                role_score=Decimal("10"),
            )
            for i in range(1, 7)
        ]
        role2_users = [
            UserProjectScore(
                user_id=i + 10,
                project_role_id=2,
                competence_match=Decimal(str(10 - i)),
                role_score=Decimal("10"),
            )
            for i in range(1, 4)
        ]
        assignments = role1_users + role2_users

        teams = match_utils.assign_unbalanced_teams(assignments, roles, num_teams=3)

        expected_role1_teams = [[9, 8], [7, 6], [5, 4]]
        for team_idx, team in enumerate(teams):
            role1_vals = [u.competence_match for u in team if u.project_role_id == 1]
            assert role1_vals == [
                Decimal(str(v)) for v in expected_role1_teams[team_idx]
            ]

        expected_role2_teams = [[9], [8], [7]]
        for team_idx, team in enumerate(teams):
            role2_vals = [u.competence_match for u in team if u.project_role_id == 2]
            assert role2_vals == [
                Decimal(str(v)) for v in expected_role2_teams[team_idx]
            ]

    def test_team_sizes(self, match_utils):
        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=101, description=None, quantity_per_team=3
            ),
            ProjectRole(
                id=2, project_id=1, role_id=102, description=None, quantity_per_team=2
            ),
            ProjectRole(
                id=3, project_id=1, role_id=103, description=None, quantity_per_team=1
            ),
        ]
        assignments = []
        num_teams = 4
        teams = match_utils.assign_unbalanced_teams(assignments, roles, num_teams)

        expected_size_per_team = sum(r.quantity_per_team for r in roles)  # 3+2+1 = 6
        for team in teams:
            assert len(team) == expected_size_per_team

    def test_dummy_users_have_fake_user_id(self, match_utils, sample_roles):
        assignments = []
        num_teams = 2
        teams = match_utils.assign_unbalanced_teams(
            assignments, sample_roles, num_teams
        )

        for team in teams:
            for user in team:
                assert user.user_id == match_utils.fake_user_id
                assert user.competence_match == Decimal(0)
                assert user.role_score == Decimal(0)

    def test_empty_assignments_and_roles(self, match_utils):
        teams = match_utils.assign_unbalanced_teams([], [], num_teams=3)
        assert teams == [[] for _ in range(3)]

    def test_sorting_descending(self, match_utils):
        roles = [
            ProjectRole(
                id=1, project_id=1, role_id=101, description=None, quantity_per_team=1
            )
        ]
        assignments = [
            UserProjectScore(
                user_id=1,
                project_role_id=1,
                competence_match=Decimal("0.5"),
                role_score=Decimal("10"),
            ),
            UserProjectScore(
                user_id=2,
                project_role_id=1,
                competence_match=Decimal("0.9"),
                role_score=Decimal("10"),
            ),
            UserProjectScore(
                user_id=3,
                project_role_id=1,
                competence_match=Decimal("0.2"),
                role_score=Decimal("10"),
            ),
            UserProjectScore(
                user_id=4,
                project_role_id=1,
                competence_match=Decimal("0.7"),
                role_score=Decimal("10"),
            ),
        ]
        num_teams = 2
        teams = match_utils.assign_unbalanced_teams(assignments, roles, num_teams)

        assert teams[0][0].competence_match == Decimal("0.9")
        assert teams[1][0].competence_match == Decimal("0.7")


class TestBalanceTeams:
    def test_balance_teams_reduces_difference(self, match_utils, sample_roles):
        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("10"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=2,
                    project_role_id=1,
                    competence_match=Decimal("9"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=3,
                    project_role_id=2,
                    competence_match=Decimal("10"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=4,
                    project_role_id=1,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=5,
                    project_role_id=1,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=6,
                    project_role_id=2,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
            ],
        ]
        original_sums = [sum(u.competence_match for u in team) for team in teams]
        assert original_sums[0] - original_sums[1] == Decimal("25")

        balanced_teams = match_utils.balance_teams(deepcopy(teams), sample_roles)
        balanced_sums = [
            sum(u.competence_match for u in team) for team in balanced_teams
        ]
        new_diff = max(balanced_sums) - min(balanced_sums)

        assert new_diff == Decimal("7.0")
        assert sum(balanced_sums) == sum(original_sums)

    def test_balance_teams_removes_dummy_users(self, match_utils, sample_roles):
        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=match_utils.fake_user_id,
                    project_role_id=1,
                    competence_match=Decimal("0"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=2,
                    project_role_id=2,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=3,
                    project_role_id=1,
                    competence_match=Decimal("4"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=match_utils.fake_user_id,
                    project_role_id=1,
                    competence_match=Decimal("0"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=4,
                    project_role_id=2,
                    competence_match=Decimal("4"),
                    role_score=Decimal("0"),
                ),
            ],
        ]
        balanced = match_utils.balance_teams(teams, sample_roles)
        for team in balanced:
            assert all(user.user_id != match_utils.fake_user_id for user in team)

    def test_balance_teams_no_change_if_already_balanced(
        self, match_utils, sample_roles
    ):
        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=2,
                    project_role_id=1,
                    competence_match=Decimal("3"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=3,
                    project_role_id=2,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=4,
                    project_role_id=1,
                    competence_match=Decimal("4"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=5,
                    project_role_id=1,
                    competence_match=Decimal("4"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=6,
                    project_role_id=2,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),
            ],
        ]
        original_teams = deepcopy(teams)
        balanced = match_utils.balance_teams(teams, sample_roles)
        for i in range(len(teams)):
            assert {u.user_id for u in original_teams[i]} == {
                u.user_id for u in balanced[i]
            }

    def test_balance_teams_respects_quantity_per_team(self, match_utils):
        roles = [
            ProjectRole(
                id=1, project_id=1, description=None, role_id=1, quantity_per_team=2
            ),
            ProjectRole(
                id=2, project_id=1, description=None, role_id=2, quantity_per_team=1
            ),
        ]
        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("9"),
                    role_score=Decimal("0"),
                ),  #
                UserProjectScore(
                    user_id=2,
                    project_role_id=1,
                    competence_match=Decimal("8"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=3,
                    project_role_id=2,
                    competence_match=Decimal("9"),
                    role_score=Decimal("0"),
                ),  #
            ],
            [
                UserProjectScore(
                    user_id=4,
                    project_role_id=1,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),  #
                UserProjectScore(
                    user_id=5,
                    project_role_id=1,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),  #
                UserProjectScore(
                    user_id=6,
                    project_role_id=2,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=7,
                    project_role_id=1,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),  # 15 8 4 1
                UserProjectScore(
                    user_id=8,
                    project_role_id=1,
                    competence_match=Decimal("6"),
                    role_score=Decimal("0"),
                ),  # 16 3 5 7
                UserProjectScore(
                    user_id=9,
                    project_role_id=2,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),  # 15 9 5 2
            ],
        ]
        balanced = match_utils.balance_teams(deepcopy(teams), roles)
        for team in balanced:
            role1_count = sum(1 for u in team if u.project_role_id == 1)
            role2_count = sum(1 for u in team if u.project_role_id == 2)
            assert role1_count == 2
            assert role2_count == 1
        sums_after = [sum([u.competence_match for u in team]) for team in balanced]
        sums_before = [sum([u.competence_match for u in team]) for team in teams]

        assert sums_after < sums_before

    def test_balance_teams_with_one_team(self, match_utils, sample_roles):
        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("10"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=2,
                    project_role_id=1,
                    competence_match=Decimal("20"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=3,
                    project_role_id=2,
                    competence_match=Decimal("30"),
                    role_score=Decimal("0"),
                ),
            ]
        ]
        balanced = match_utils.balance_teams(teams, sample_roles)
        assert len(balanced) == 1
        assert balanced[0] == teams[0]

    def test_balance_teams_with_fake_users_and_real_mix(
        self, match_utils, sample_roles
    ):

        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("10"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=match_utils.fake_user_id,
                    project_role_id=1,
                    competence_match=Decimal("0"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=2,
                    project_role_id=2,
                    competence_match=Decimal("10"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=3,
                    project_role_id=1,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=4,
                    project_role_id=1,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=match_utils.fake_user_id,
                    project_role_id=2,
                    competence_match=Decimal("0"),
                    role_score=Decimal("0"),
                ),
            ],
        ]
        balanced = match_utils.balance_teams(deepcopy(teams), sample_roles)
        print(balanced)
        for team in balanced:
            assert all(u.user_id != match_utils.fake_user_id for u in team)
        sums_after = [sum(u.competence_match for u in team) for team in balanced]
        diff_after = max(sums_after) - min(sums_after)
        assert diff_after == 1

    def test_balance_teams_stops_after_max_iter(self, match_utils, sample_roles):
        teams = [
            [
                UserProjectScore(
                    user_id=1,
                    project_role_id=1,
                    competence_match=Decimal("100"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=2,
                    project_role_id=1,
                    competence_match=Decimal("99"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=3,
                    project_role_id=2,
                    competence_match=Decimal("100"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=4,
                    project_role_id=1,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=5,
                    project_role_id=1,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=6,
                    project_role_id=2,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
            ],
        ]
        match_utils.balance_teams(deepcopy(teams), sample_roles, max_iter=1000)

    def test_balance_teams_preserves_user_ids(self, match_utils, sample_roles):
        teams = [
            [
                UserProjectScore(
                    user_id=10,
                    project_role_id=1,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=11,
                    project_role_id=1,
                    competence_match=Decimal("4"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=12,
                    project_role_id=2,
                    competence_match=Decimal("5"),
                    role_score=Decimal("0"),
                ),
            ],
            [
                UserProjectScore(
                    user_id=13,
                    project_role_id=1,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=14,
                    project_role_id=1,
                    competence_match=Decimal("2"),
                    role_score=Decimal("0"),
                ),
                UserProjectScore(
                    user_id=15,
                    project_role_id=2,
                    competence_match=Decimal("1"),
                    role_score=Decimal("0"),
                ),
            ],
        ]
        all_real_ids = {u.user_id for team in teams for u in team}
        balanced = match_utils.balance_teams(deepcopy(teams), sample_roles)
        balanced_real_ids = {u.user_id for team in balanced for u in team}
        assert balanced_real_ids == all_real_ids
