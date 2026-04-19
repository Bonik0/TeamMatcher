import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.interfaces.use_case import IUseCase


class EmailSendUseCase(IUseCase):
    def __init__(self, server: str, port: int, login: str, password: str) -> None:
        self.server = server
        self.port = port
        self.login = login
        self.password = password

    def _get_message(
        self, receiver_email: str, subject: str, text: MIMEText
    ) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self.login
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(text)
        return message

    async def execute(self, receiver_email: str, subject: str, text: MIMEText) -> None:
        message = self._get_message(receiver_email, subject, text)
        server = smtplib.SMTP(self.server, self.port)
        server.starttls()
        server.login(self.login, self.password)
        server.sendmail(self.login, receiver_email, message.as_string())
        server.quit()
