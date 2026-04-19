from email.mime.text import MIMEText
from core.entities import VerificationCode
from app.base.use_cases import EmailSendUseCase
import aiohttp


class VerifyCodeEmailSendUseCase(EmailSendUseCase):
    def __init__(
        self, server: str, port: int, login: str, password: str, page_url: str
    ) -> None:
        super().__init__(server, port, login, password)
        self.page_url = page_url

    async def execute(self, verification_code: VerificationCode) -> None:
        subject = f"{verification_code.code} is your verification code"

        async with aiohttp.ClientSession() as session:
            email_response = await session.get(
                url=self.page_url, params={"code": verification_code.code}
            )
            email_html = await email_response.text()
            await super().execute(
                verification_code.email, subject, MIMEText(email_html, "html")
            )
