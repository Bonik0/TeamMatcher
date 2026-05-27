import networkx as nx
from core.entities import (
    UserProjectScore,
    UserWithFormsAndCompetences,
    ProjectRoleWithCompetences,
    ProjectRole,
)
from app.match.utils.interfaces import (
    ICompetenceSimilarityUtils,
    IMatchUtils,
    IUserProjectRoleSimilarityUtils,
)
import math
from collections import defaultdict
from decimal import Decimal
from copy import deepcopy
import random
import logging


class MatchUtils(IMatchUtils):
    def __init__(
        self,
        competence_utils: ICompetenceSimilarityUtils,
        similarity_utils: IUserProjectRoleSimilarityUtils,
        fake_user_id: int = -1,
        initial_temp: float = 5000.0,
        cooling_rate: float = 0.998,
        temp_min: float = 0.01,
        steps_per_temp_factor: int = 5,
        random_seed: int | None = None,
    ) -> None:
        self.competence_utils = competence_utils
        self.similarity_utils = similarity_utils
        self.fake_user_id = fake_user_id
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.temp_min = temp_min
        self.steps_per_temp_factor = steps_per_temp_factor
        random.seed(random_seed)

    def get_max_teams_number(
        self, project_roles: list[ProjectRole], users_count: int
    ) -> int:
        return math.ceil(
            users_count
            / sum(project_role.quantity_per_team for project_role in project_roles)
        )

    def compute_scores(
        self,
        users: list[UserWithFormsAndCompetences],
        project_roles: list[ProjectRoleWithCompetences],
    ) -> list[UserProjectScore]:
        users_project_scores = []
        for user in users:
            for role in project_roles:
                competence_match = self.competence_utils.execute(
                    project_competences=role.competences,
                    user_competences=user.competences,
                )
                final_score = self.similarity_utils.execute(
                    competence_match=competence_match,
                    user_roles=user.forms,
                    project_role_id=role.id,
                )
                user_project_score = UserProjectScore(
                    user_id=user.id,
                    project_role_id=role.id,
                    competence_match=competence_match,
                    role_score=final_score,
                )
                users_project_scores.append(user_project_score)
        return users_project_scores

    def assign_roles(
        self,
        users_project_scores: list[UserProjectScore],
        project_roles: list[ProjectRole],
        num_teams: int,
    ) -> list[UserProjectScore]:

        if not users_project_scores or not project_roles or num_teams < 1:
            return []

        G = nx.DiGraph()
        source = "source"
        sink = "sink"

        max_user_score = max(
            user_score.role_score for user_score in users_project_scores
        )
        total_vacancies = sum(
            project_role.quantity_per_team * num_teams for project_role in project_roles
        )
        user_ids = {
            user_project_score.user_id for user_project_score in users_project_scores
        }
        user_nodes = {user_id: f"user_{user_id}" for user_id in user_ids}
        role_nodes = {
            project_role.id: f"role_{project_role.id}" for project_role in project_roles
        }

        G.add_node(source, demand=-total_vacancies)
        G.add_node(sink, demand=total_vacancies)

        for user_node in user_nodes.values():
            G.add_edge(source, user_node, capacity=1, weight=0)

        for project_role in project_roles:
            role_node = role_nodes[project_role.id]
            capacity = project_role.quantity_per_team * num_teams
            G.add_edge(role_node, sink, capacity=capacity, weight=0)

        for user_score in users_project_scores:
            user_node = user_nodes[user_score.user_id]
            role_node = role_nodes[user_score.project_role_id]
            weight = max_user_score - user_score.role_score
            G.add_edge(user_node, role_node, capacity=1, weight=weight)

        flow_dict = nx.max_flow_min_cost(G, source, sink)

        assignments: list[UserProjectScore] = []

        for user_score in users_project_scores:
            user_node = user_nodes[user_score.user_id]
            role_node = role_nodes[user_score.project_role_id]
            if flow_dict.get(user_node, {}).get(role_node, 0) > 0:
                assignments.append(user_score)

        return assignments

    def assign_unbalanced_teams(
        self,
        assignments: list[UserProjectScore],
        project_roles: list[ProjectRole],
        num_teams: int,
    ) -> list[list[UserProjectScore]]:
        role_to_users: dict[int, list[UserProjectScore]] = defaultdict(list)

        for assignment in assignments:
            role_to_users[assignment.project_role_id].append(assignment)

        for project_role in project_roles:
            need_users_count = num_teams * project_role.quantity_per_team
            user_assignments = role_to_users.get(project_role.id) or []
            for _ in range(need_users_count - len(user_assignments)):
                user_assignments.append(
                    UserProjectScore(
                        user_id=self.fake_user_id,
                        project_role_id=project_role.id,
                        competence_match=Decimal(0),
                        role_score=Decimal(0),
                    )
                )
            user_assignments.sort(
                key=lambda assignment: assignment.competence_match, reverse=True
            )
            role_to_users[project_role.id] = user_assignments[:need_users_count]

        teams: list[list[UserProjectScore]] = [[] for _ in range(num_teams)]

        for project_role in project_roles:
            quantity = project_role.quantity_per_team
            project_role_id = project_role.id

            for team_index in range(num_teams):
                teams[team_index].extend(
                    role_to_users[project_role_id][
                        (team_index) * quantity : (team_index + 1) * quantity
                    ]
                )
        return teams

    def balance_teams(
        self,
        teams: list[list[UserProjectScore]],
        project_roles: list[ProjectRole],
    ) -> list[list[UserProjectScore]]:
        objective = lambda team_sums: max(team_sums) - min(team_sums)

        num_teams = len(teams)
        steps_per_temp = max(10, self.steps_per_temp_factor * num_teams)
        T = self.initial_temp

        if num_teams < 2:
            return teams

        role_ids = [project_role.id for project_role in project_roles]
        team_sums = [
            float(sum(user.competence_match for user in team)) for team in teams
        ]

        current_score = objective(team_sums)

        best_score = current_score
        best_teams = deepcopy(teams)

        while T > self.temp_min:
            for _ in range(steps_per_temp):
                team_i, team_j = random.sample(range(num_teams), 2)
                role_id = random.choice(role_ids)

                members_index_i = [
                    index
                    for index, user in enumerate(teams[team_i])
                    if user.project_role_id == role_id
                ]
                members_index_j = [
                    index
                    for index, user in enumerate(teams[team_j])
                    if user.project_role_id == role_id
                ]

                member_i = random.choice(members_index_i)
                member_j = random.choice(members_index_j)
                member_competence_i = float(teams[team_i][member_i].competence_match)
                member_competence_j = float(teams[team_j][member_j].competence_match)

                new_sum_i = (
                    team_sums[team_i] - member_competence_i + member_competence_j
                )
                new_sum_j = (
                    team_sums[team_j] - member_competence_j + member_competence_i
                )

                temp_sums = team_sums.copy()
                temp_sums[team_i] = new_sum_i
                temp_sums[team_j] = new_sum_j
                new_score = objective(temp_sums)

                delta = new_score - current_score

                if delta < 0 or random.random() < math.exp(-delta / T):
                    teams[team_i][member_i], teams[team_j][member_j] = (
                        teams[team_j][member_j],
                        teams[team_i][member_i],
                    )
                    team_sums[team_i] = new_sum_i
                    team_sums[team_j] = new_sum_j
                    current_score = new_score

                    if current_score < best_score:
                        best_teams = deepcopy(teams)
                        best_score = current_score
                        logging.info(f"{best_score=}")


            T *= self.cooling_rate

        for team in best_teams:
            team[:] = [user for user in team if user.user_id != self.fake_user_id]

        return best_teams

    def execute(
        self,
        users: list[UserWithFormsAndCompetences],
        project_roles: list[ProjectRoleWithCompetences],
    ) -> list[list[UserProjectScore]]:
        user_scores = self.compute_scores(users, project_roles)
        team_number = self.get_max_teams_number(project_roles, len(users))
        assignments = self.assign_roles(user_scores, project_roles, team_number)
        teams = self.assign_unbalanced_teams(assignments, project_roles, team_number)
        return self.balance_teams(teams, project_roles)
