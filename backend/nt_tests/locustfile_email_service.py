from locust import HttpUser, task, between
import random
import string
import uuid


def _random_email() -> str:
    name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{name}@example.com"


def _random_op_id() -> str:
    return str(uuid.uuid4())


class EmailServiceUser(HttpUser):
    wait_time = between(0.0, 0.0)

    emails = [_random_email()]
    email_to_op_id = {emails[0]: _random_op_id()}

    @task(5)
    def send_code(self) -> None:
        email = _random_email()
        response = self.client.post(
            "/code/send", json={"email": email}, catch_response=True
        )
        if response.status_code != 200:
            return
        op_id = response.json().get("operation_id")
        self.email_to_op_id[email] = op_id
        self.emails.append(email)

    @task(1)
    def verify_wrong_code(self) -> None:
        email = random.choice(self.emails)
        op_id = self.email_to_op_id[email]
        code = random.randint(10**5, 10**6 - 1)
        self.client.post(
            "/code/verify", json={"email": email, "code": code, "operation_id": op_id}
        )

    @task(5)
    def verify_wrong_op_id(self) -> None:
        email = _random_email()
        op_id = _random_op_id()
        code = random.randint(10**5, 10**6 - 1)
        self.client.post(
            "/code/verify", json={"email": email, "code": code, "operation_id": op_id}
        )
