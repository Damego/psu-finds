from src.observers.events.user import UserCreatedEvent
from src.services.send_email_service import EmailService
from src.utils.abstract.observer import Observer


class UserCreatedEmailObserver(Observer):
    def __init__(self, service: EmailService):
        self.service: EmailService = service

    def accept(self, event: UserCreatedEvent):
        self.service.send_account_verification_email(event.email, event.verification_code)
