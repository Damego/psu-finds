import requests

from src.settings import settings

ENDPOINT = "https://api.beta.rusender.ru/api/v1/external-mails/send"


class EmailSenderRepository:
    @staticmethod
    def send_email(target: str, title: str, content: str):
        raise NotImplementedError


class RuSenderRepository(EmailSenderRepository):
    @staticmethod
    def send_email(target: str, title: str, content: str):
        payload = {
            "mail": {
                "to": {"email": target, "name": "user"},
                "from": {"email": "no-reply@damego.ru", "name": "Бюро находок"},
                "subject": title,
                "html": content,
            }
        }
        response = requests.post(
            ENDPOINT, json=payload, headers={"X-Api-Key": settings.RUSENDER_API_KEY}
        )

        if response.status_code == 200:
            return response.json()

        print(response.json())
        # TODO: provide 4xx handler https://rusender.ru/developer/api/email/