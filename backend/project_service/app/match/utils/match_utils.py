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


class MatchUtils(IMatchUtils):
    def __init__(
        self,
        competence_utils: ICompetenceSimilarityUtils,
        similarity_utils: IUserProjectRoleSimilarityUtils,
        fake_user_id: int = -1,
    ) -> None:
        self.competence_utils = competence_utils
        self.similarity_utils = similarity_utils
        self.fake_user_id = fake_user_id

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
        max_iter: int = 1000,
    ) -> list[list[UserProjectScore]]:

        num_teams = len(teams)
        team_sums = [sum(user.competence_match for user in team) for team in teams]

        improved = True
        iter_count = 0

        while improved and iter_count < max_iter:
            improved = False
            iter_count += 1

            max_index = max(range(num_teams), key=lambda i: team_sums[i])
            min_index = min(range(num_teams), key=lambda i: team_sums[i])

            if team_sums[max_index] == team_sums[min_index]:
                break

            current_diff = team_sums[max_index] - team_sums[min_index]

            for k in range(num_teams):
                if k == max_index or k == min_index:
                    continue

                for role in project_roles:
                    user_k = next(
                        (user for user in teams[k] if user.project_role_id == role.id),
                        None,
                    )
                    user_max = next(
                        (
                            user
                            for user in teams[max_index]
                            if user.project_role_id == role.id
                        ),
                        None,
                    )
                    if (
                        user_k
                        and user_max
                        and user_k.competence_match < user_max.competence_match
                    ):
                        new_sum_max = (
                            team_sums[max_index]
                            - user_max.competence_match
                            + user_k.competence_match
                        )
                        new_sum_k = (
                            team_sums[k]
                            - user_k.competence_match
                            + user_max.competence_match
                        )

                        new_sums = team_sums.copy()
                        new_sums[max_index] = new_sum_max
                        new_sums[k] = new_sum_k

                        new_diff = max(new_sums) - min(new_sums)
                        if abs(new_diff) < current_diff:
                            index_max = teams[max_index].index(user_max)
                            index_k = teams[k].index(user_k)

                            teams[max_index][index_max], teams[k][index_k] = (
                                teams[k][index_k],
                                teams[max_index][index_max],
                            )
                            team_sums[max_index] = new_sum_max
                            team_sums[k] = new_sum_k

                            improved = True
                            current_diff = new_diff
                if improved:
                    break

                for role in project_roles:
                    user_k = next(
                        (user for user in teams[k] if user.project_role_id == role.id),
                        None,
                    )
                    user_min = next(
                        (
                            user
                            for user in teams[min_index]
                            if user.project_role_id == role.id
                        ),
                        None,
                    )
                    if (
                        user_k
                        and user_min
                        and user_k.competence_match > user_min.competence_match
                    ):
                        new_sum_min = (
                            team_sums[min_index]
                            - user_min.competence_match
                            + user_k.competence_match
                        )
                        new_sum_k = (
                            team_sums[k]
                            - user_k.competence_match
                            + user_min.competence_match
                        )

                        new_sums = team_sums.copy()
                        new_sums[min_index] = new_sum_min
                        new_sums[k] = new_sum_k

                        new_diff = max(new_sums) - min(new_sums)
                        if abs(new_diff) < current_diff:
                            index_min = teams[min_index].index(user_min)
                            index_k = teams[k].index(user_k)
                            teams[min_index][index_min], teams[k][index_k] = (
                                teams[k][index_k],
                                teams[min_index][index_min],
                            )
                            team_sums[min_index] = new_sum_min
                            team_sums[k] = new_sum_k
                            improved = True
                            current_diff = new_diff
                            break
                if improved:
                    break

            if not improved:
                for role in project_roles:
                    users_max = [
                        user
                        for user in teams[max_index]
                        if user.project_role_id == role.id
                    ]
                    users_min = [
                        user
                        for user in teams[min_index]
                        if user.project_role_id == role.id
                    ]
                    for user_max in users_max:
                        for user_min in users_min:
                            if user_max.competence_match > user_min.competence_match:
                                new_sum_max = (
                                    team_sums[max_index]
                                    - user_max.competence_match
                                    + user_min.competence_match
                                )
                                new_sum_min = (
                                    team_sums[min_index]
                                    - user_min.competence_match
                                    + user_max.competence_match
                                )
                                new_diff = new_sum_max - new_sum_min
                                if abs(new_diff) < current_diff:
                                    idx_max = teams[max_index].index(user_max)
                                    idx_min = teams[min_index].index(user_min)
                                    (
                                        teams[max_index][idx_max],
                                        teams[min_index][idx_min],
                                    ) = (
                                        teams[min_index][idx_min],
                                        teams[max_index][idx_max],
                                    )
                                    team_sums[max_index] = new_sum_max
                                    team_sums[min_index] = new_sum_min
                                    improved = True
                                    break
                        if improved:
                            break
                    if improved:
                        break

        for team in teams:
            team[:] = [user for user in team if user.user_id != self.fake_user_id]

        return teams

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
