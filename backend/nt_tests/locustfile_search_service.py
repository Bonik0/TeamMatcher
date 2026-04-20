from locust import HttpUser, task, between
import random
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "backend" / "migration_service" / "migration" / "synthetic_data"


def _load_csv_ids(filename: str) -> list[int]:
    path = DATA_DIR / filename
    ids = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append(row.get("id"))
    return ids


def _load_csv_names(filename: str) -> list[int]:
    path = DATA_DIR / filename
    names = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row.get("name"))
    return names


ROLE_IDS, ROLE_NAMES = _load_csv_ids("roles.csv"), _load_csv_names("roles.csv")
COMPETENCE_IDS, COMPETENCE_NAMES = (
    _load_csv_ids("competences.csv"),
    _load_csv_names("competences.csv"),
)
PROJECT_IDS, PROJECT_NAMES = (
    _load_csv_ids("project.csv"),
    _load_csv_names("project.csv"),
)


def _random_query_from_name_list(names: list[str]) -> str:
    name = random.choice(names)
    return name[random.randint(0, 2) : random.randint(4, 10)]


class SearchServiceUser(HttpUser):
    wait_time = between(0, 0)

    @task
    def role_search(self) -> None:
        q = _random_query_from_name_list(ROLE_NAMES)
        params = {"q": q, "limit": 10, "offset": random.randint(0, 50)}
        self.client.get("/search/role", params=params, name="/search/role")

    @task
    def competence_search(self) -> None:
        q = _random_query_from_name_list(COMPETENCE_NAMES)
        params = {"q": q, "limit": 10, "offset": random.randint(0, 50)}
        self.client.get("/search/competence", params=params, name="/search/competence")

    @task
    def project_search(self) -> None:
        q = _random_query_from_name_list(PROJECT_NAMES)
        role_choices = random.sample(ROLE_IDS, k=random.randint(0, len(ROLE_IDS)))
        comp_choices = random.sample(
            COMPETENCE_IDS, k=random.randint(0, len(COMPETENCE_IDS))
        )
        params = [("q", q), ("limit", 10), ("offset", random.randint(0, 50))]
        for r in role_choices:
            params.append(("role_ids", r))
        for c in comp_choices:
            params.append(("competence_ids", c))
        self.client.get("/search/project", params=params, name="/search/project")

    @task
    def project_by_id(self) -> None:
        pid = random.choice(PROJECT_IDS)
        self.client.get(f"/search/project/{pid}", name="/search/project/{id}")
