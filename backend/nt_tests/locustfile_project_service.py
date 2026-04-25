from locust import HttpUser, task, between
import random
import csv
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Any
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "backend" / "migration_service" / "migration" / "synthetic_data"
USERS_CSV = DATA_DIR / "users.csv"
PROJECTS_CSV = DATA_DIR / "project.csv"
ROLE_CSV = DATA_DIR / "roles.csv"
COMPETENCE_CSV = DATA_DIR / "competences.csv"
ROLE_TO_COMPETENCE_CSV = DATA_DIR / "role_to_competence.csv"


def _load_organizer_emails() -> list[str]:
    emails = []
    with open(USERS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("role") == "organizer":
                emails.append(row["email"])
    return emails


def _load_project_ids() -> list[int]:
    ids = []
    with open(PROJECTS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append(int(row["id"]))
    return ids


def _load_role_ids_and_names() -> list[tuple[int, str]]:
    ids_and_names = []
    with open(ROLE_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids_and_names.append((int(row["id"]), row["name"]))
    return ids_and_names


def _load_competence_ids_and_names() -> list[tuple[int, str]]:
    ids_and_names = []
    with open(COMPETENCE_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids_and_names.append((int(row["id"]), row["name"]))
    return ids_and_names


def _load_role_to_competence(
    competences: list[tuple[int, str]],
) -> dict[int, list[dict[str, str | int]]]:
    role_to_competence = defaultdict(list)
    with open(ROLE_TO_COMPETENCE_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            role_to_competence[int(row["role_id"])].append(
                {
                    "name": next(
                        (
                            name
                            for id, name in competences
                            if id == int(row["competence_id"])
                        ),
                        None,
                    ),
                    "importance": int(row["importance"]),
                }
            )
    return role_to_competence


ORGANIZERS = _load_organizer_emails()
PROJECT_IDS = _load_project_ids()
ROLE_IDS_AND_NAMES = _load_role_ids_and_names()
COMPETENCE_IDS_AND_NAMES = _load_competence_ids_and_names()
ROLE_TO_COMPETENCE = _load_role_to_competence(COMPETENCE_IDS_AND_NAMES)

AUTH_HOST = "http://localhost:8005"
DEFAULT_PASSWORD = "123321"


def _make_role(role_id: int, role_name: str) -> dict[str, Any]:
    return {
        "name": role_name,
        "description": None,
        "quantity_per_team": random.randint(1, 3),
        "competences": ROLE_TO_COMPETENCE[role_id],
    }


def _random_roles() -> list[tuple[int, str]]:
    return list(set(random.choices(ROLE_IDS_AND_NAMES, k=random.randint(1, 5))))


def _random_project_payload(roles: list[tuple[int, str]]) -> dict[str, Any]:

    return {
        "name": f"load-{uuid4().hex[:8]}",
        "description": "load test project",
        "start_time": (datetime.now() + timedelta(days=random.randint(5, 30))).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "roles": [_make_role(role_id, role_name) for role_id, role_name in roles],
    }


class ProjectServiceUser(HttpUser):
    wait_time = between(0, 0)

    def on_start(self) -> None:
        self.email = random.choice(ORGANIZERS)
        self.project_id = None
        self.roles = None
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
    def find_all_projects(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.get("/", headers=headers, name="/organizer/")

    @task(20)
    def get_project_teams(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.get("/teams", headers=headers, name="/organizer/teams")

    @task(25)
    def create_project(self) -> None:
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        roles = _random_roles()
        payload = _random_project_payload(roles)
        response = self.client.put(
            "/", json=payload, headers=headers, name="/organizer/ (create)"
        )
        if response.status_code == 201:
            self.project_id = response.json().get("project_id")
            self.roles = roles

    @task(15)
    def update_project(self) -> None:
        if not self.project_id:
            return
        payload = {
            "project_id": int(self.project_id),
            "name": f"updated-{uuid4().hex[:6]}",
            "description": "updated",
            "start_time": (datetime.now() + timedelta(days=10)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "roles": [
                _make_role(role_id, role_name) for role_id, role_name in self.roles
            ],
        }
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.post(
            "/", json=payload, headers=headers, name="/organizer/ (update)"
        )

    @task(10)
    def cancel_project(self) -> None:
        if not self.project_id:
            return
        payload = {"project_id": int(self.project_id)}
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.post(
            "/cancel", json=payload, headers=headers, name="/organizer/ (cancel)"
        )
        self.project_id = None
        self.roles = None

    @task(10)
    def form_teams(self) -> None:
        if not self.project_id:
            return
        payload = {"project_id": int(self.project_id)}
        headers = (
            {"Authorization": f"Bearer {self.access_token}"}
            if self.access_token
            else {}
        )
        self.client.post(
            "/match", json=payload, headers=headers, name="/organizer/match"
        )
        self.project_id = None
        self.roles = None
