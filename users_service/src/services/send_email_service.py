from ..repositories.email_sender_repository import EmailSenderStrategy


class EmailService:
    def __init__(self, repository: EmailSenderStrategy):
        self.repository: EmailSenderStrategy = repository

    def send_account_verification_email(self, email: str, code: str):
        title = "Подтверждение аккаунта"
        content = f"Код подтверждения аккаунта: {code}"
        self.repository.send_email(email, title, content)
