from src.repositories.email_sender_repository import EmailSenderRepository


class EmailService:
    def __init__(self, repository: EmailSenderRepository):
        self.repository: EmailSenderRepository = repository

    def send_account_verification_email(self, email: str, code: str):
        title = "Подтверждение аккаунта"
        content = f"Код подтверждения аккаунта: {code}"
        self.repository.send_email(email, title, content)
