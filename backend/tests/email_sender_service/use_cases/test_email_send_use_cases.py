from email.mime.text import MIMEText
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from email_sender_service.app.base.use_cases import EmailSendUseCase
from email_sender_service.app.verification_code.use_cases import (
    VerifyCodeEmailSendUseCase,
)
from core.entities import VerificationCode


class MockAsyncContextManager:
    def __init__(self, sess):
        self.sess = sess

    async def __aenter__(self):
        return self.sess

    async def __aexit__(self, exc_type, exc, tb):
        return None


def test_get_message_sets_headers_and_body() -> None:
    use_case = EmailSendUseCase("smtp.example.com", 25, "me@example.com", "pass")
    text = MIMEText("<p>Hello</p>", "html")
    msg = use_case._get_message("you@example.com", "Subject", text)

    assert msg["From"] == "me@example.com"
    assert msg["To"] == "you@example.com"
    assert msg["Subject"] == "Subject"
    assert any(part.get_payload() == "<p>Hello</p>" for part in msg.get_payload())


@pytest.mark.asyncio
async def test_execute_uses_smtp_and_sends_message(monkeypatch) -> None:
    use_case = EmailSendUseCase("smtp.example.com", 587, "me@example.com", "pass")
    text = MIMEText("Hi", "plain")

    mock_server = MagicMock()
    mock_server.starttls = MagicMock()
    mock_server.login = MagicMock()
    mock_server.sendmail = MagicMock()
    mock_server.quit = MagicMock()

    with patch(
        "email_sender_service.app.base.use_cases.smtplib.SMTP", return_value=mock_server
    ) as smtp_mock:
        await use_case.execute("you@example.com", "Subject", text)

    smtp_mock.assert_called_once_with("smtp.example.com", 587)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("me@example.com", "pass")
    mock_server.sendmail.assert_called_once()
    mock_server.quit.assert_called_once()


@pytest.mark.asyncio
async def test_verify_code_email_send_fetches_template_and_calls_super_execute() -> (
    None
):
    op_id = uuid4()
    vc = VerificationCode(email="a@a.com", code=1234, operation_id=op_id)

    response = SimpleNamespace()
    response.text = AsyncMock(return_value="<html>code</html>")

    session = SimpleNamespace()
    session.get = AsyncMock(return_value=response)

    with patch(
        "email_sender_service.app.verification_code.use_cases.aiohttp.ClientSession",
        return_value=MockAsyncContextManager(session),
    ):
        with patch(
            "email_sender_service.app.verification_code.use_cases.EmailSendUseCase.execute",
            new_callable=AsyncMock,
        ) as parent_exec:
            use_case = VerifyCodeEmailSendUseCase("smtp", 25, "l", "p", "http://page")
            await use_case.execute(vc)

    session.get.assert_awaited_once_with(url="http://page", params={"code": 1234})
    parent_exec.assert_awaited_once()
