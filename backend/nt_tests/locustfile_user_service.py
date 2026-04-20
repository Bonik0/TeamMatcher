from locust import HttpUser, task, between
import random
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "backend" / "migration_service" / "migration" / "synthetic_data"
USERS_CSV = DATA_DIR / "users.csv"
PROJECTS_CSV = DATA_DIR / "project.csv"
PROJECT_ROLES_CSV = DATA_DIR / "project_role.csv"
COMPETENCE_CSV = DATA_DIR / "competences.csv"


def _load_user_emails() -> list[str]:
    emails = []
    with open(USERS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("role") == "user":
                emails.append(row["email"])
    return emails


def _load_project_ids() -> list[int]:
    ids = []
    with open(PROJECTS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append(int(row["id"]))
    return ids


def _load_competence_ids() -> list[int]:
    ids_and_names = []
    with open(COMPETENCE_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids_and_names.append(int(row["id"]))
    return ids_and_names


def _load_project_roles() -> list[tuple[int, int]]:
    roles = []
    with open(PROJECT_ROLES_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            roles.append((int(row["id"]), int(row["project_id"])))
    return roles


USER_EMAILS = _load_user_emails()
PROJECT_IDS = _load_project_ids()
COMPETENCE_IDS = _load_competence_ids()
PROJECT_ROLES = _load_project_roles()


DEFAULT_PASSWORD = "123321"
AUTH_HOST = "http://localhost:8005"


def _build_roles_for_project(project_id: int) -> list[dict[str, int]]:
    roles = [role for role in PROJECT_ROLES if role[1] == project_id]
    user_roles = list(set(random.choices(roles, k=random.randint(1, len(roles)))))

    return [
        {"project_role_id": user_role[0], "priority": index}
        for index, user_role in enumerate(user_roles, start=1)
    ]


class UserServiceUser(HttpUser):
    wait_time = between(0, 0)

    def on_start(self) -> None:
        self.email = random.choice(USER_EMAILS)
        self.access_token = None
        self.refresh_token = None
        response = self.client.post(
            f"{AUTH_HOST}/login",
            json={"email": self.email, "password": DEFAULT_PASSWORD},
        )
        if response.status_code == 200:
            js = response.json()
            self.access_token = js.get("access_token")
            self.refresh_token = js.get("refresh_token")

    @task(25)
    def get_competences(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.get("/competence", headers=headers, name="/competence (get)")

    @task(20)
    def add_competence(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        comp_id = random.choice(COMPETENCE_IDS)
        level = random.randint(1, 3)
        payload = {"competences": [{"competence_id": comp_id, "level": level}]}
        self.client.post(
            "/competence", json=payload, headers=headers, name="/competence (post)"
        )

    @task(10)
    def delete_competence(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        comp_id = random.choice(COMPETENCE_IDS)
        payload = {"competence_ids": [comp_id]}
        self.client.delete(
            "/competence", json=payload, headers=headers, name="/competence (delete)"
        )

    @task(20)
    def get_roles_for_project(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        project_id = random.choice(PROJECT_IDS)
        self.client.get(
            f"/role/project/{project_id}", headers=headers, name="/role/project/{id}"
        )

    @task(15)
    def get_all_roles(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.get("/role", headers=headers, name="/role")

    @task(20)
    def add_or_update_roles(self) -> None:
        project_id = random.choice(PROJECT_IDS)
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        roles = _build_roles_for_project(project_id)
        payload = {"project_id": project_id, "roles": roles}
        self.client.put("/role", json=payload, headers=headers, name="/role (put)")

    @task(10)
    def delete_roles(self) -> None:
        project_id = random.choice(PROJECT_IDS)
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        payload = {"project_id": project_id}
        self.client.delete(
            "/role", json=payload, headers=headers, name="/role (delete)"
        )

    @task(15)
    def get_teams(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.get("/team", headers=headers, name="/team")
