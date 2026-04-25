from locust import HttpUser, task, between
import random
import csv
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "backend" / "migration_service" / "migration" / "synthetic_data"
USERS_CSV = DATA_DIR / "users.csv"


def _load_user_emails() -> list[str]:
    emails = []
    with open(USERS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            emails.append(row["email"])
    return emails


USER_EMAILS = _load_user_emails()
DEFAULT_PASSWORD = "123321"


class AuthServiceUser(HttpUser):
    wait_time = between(0, 0)

    def on_start(self) -> None:
        self.email = random.choice(USER_EMAILS)
        self.password = DEFAULT_PASSWORD
        self.access_token = None
        self.refresh_token = None
        response = self.client.post(
            "/login", json={"email": self.email, "password": self.password}
        )
        if response.status_code == 200:
            js = response.json()
            self.access_token = js.get("access_token")
            self.refresh_token = js.get("refresh_token")

    @task(40)
    def verify_access_token(self) -> None:
        if not self.access_token:
            return
        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.client.get("/token", headers=headers, name="/token (verify)")

    @task(10)
    def update_tokens(self) -> None:
        if not self.refresh_token:
            return

        response = self.client.post(
            "/token/update",
            json={"refresh_token": self.refresh_token},
            name="/token/update",
        )
        if response.status_code == 200:
            js = response.json()
            self.access_token = js.get("access_token")
            self.refresh_token = js.get("refresh_token")

    @task(5)
    def login(self) -> None:
        if self.email is None:
            return
        response = self.client.post(
            "/login",
            json={"email": self.email, "password": DEFAULT_PASSWORD},
            name="/login",
        )
        if response.status_code == 200:
            js = response.json()
            self.access_token = js.get("access_token")
            self.refresh_token = js.get("refresh_token")

    @task(3)
    def registration(self) -> None:
        email = f"load_reg_{uuid4().hex}@example.com"
        payload = {
            "email": email,
            "password": DEFAULT_PASSWORD,
            "first_name": "Load",
            "patronymic": None,
            "surname": "Test",
            "operation_id": str(uuid4()),
        }
        response = self.client.post("/registration", json=payload, name="/registration")
        if response.status_code == 200:
            js = response.json()
            self.access_token = js.get("access_token")
            self.refresh_token = js.get("refresh_token")
            self.email = email

    @task(2)
    def organizer_registration(self) -> None:
        email = f"load_org_{uuid4().hex}@example.com"
        payload = {
            "email": email,
            "password": DEFAULT_PASSWORD,
            "first_name": "Org",
            "patronymic": None,
            "surname": "Test",
            "operation_id": str(uuid4()),
        }
        response = self.client.post(
            "/organizer-registration", json=payload, name="/organizer-registration"
        )
        if response.status_code == 200:
            js = response.json()
            self.access_token = js.get("access_token")
            self.refresh_token = js.get("refresh_token")
            self.email = email

    @task(5)
    def change_password(self) -> None:
        if not self.email:
            return
        payload = {
            "email": self.email,
            "operation_id": str(uuid4()),
            "password": DEFAULT_PASSWORD,
        }
        self.client.post("/change-password", json=payload, name="/change-password")

    @task(3)
    def logout(self) -> None:
        if not self.access_token:
            return
        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.client.get("/token/logout", headers=headers, name="/token/logout")
        self.access_token = None
        self.refresh_token = None
        self.email = None

    @task(2)
    def full_logout(self) -> None:
        if not self.access_token:
            return
        headers = {"Authorization": f"Bearer {self.access_token}"}
        self.client.get(
            "/token/full-logout", headers=headers, name="/token/full-logout"
        )
        self.access_token = None
        self.refresh_token = None
        self.email = None
