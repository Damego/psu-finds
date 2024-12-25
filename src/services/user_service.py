from typing import Optional
import random

from ..api import auth, exceptions
from ..models.schemas.users import UserCreate, UserSchema, UserUpdate
from src.utils.abstract.db_repository import Repository
from ..observers.events.user import UserCreatedEventData
from ..observers.events.base import BaseEvent
from ..observers.logger_observer import LoggerObserver
from ..utils.abstract.observer import Observer
from ..observers.email_observer import UserCreatedEmailObserver

# TODO: Replace with Redis
active_codes: dict[str, str] = {}


class UserCreatorService:
    def __init__(self, repository: Repository[UserSchema]):
        from ..api.dependencies import get_email_service

        self._observers: list[Observer] = [UserCreatedEmailObserver(get_email_service()), LoggerObserver()]
        self.repository = repository

    @staticmethod
    def _generate_code_for_email(email: str):
        code_num = random.randint(0, 99999)
        code = f"{code_num:05d}"
        active_codes[email] = code
        return code

    async def create_user(self, user_create: UserCreate) -> UserSchema:
        hashed_password = auth.get_password_hash(user_create.password)
        payload = {
            "name": user_create.name,
            "email": user_create.email,
            "hashed_password": hashed_password,
            "permissions": 0,
            "is_verified": False,
        }
        user = await self.repository.add_one(payload)

        event = BaseEvent(data=UserCreatedEventData(user=user, verification_code=self._generate_code_for_email(user.email)))
        for observer in self._observers:
            observer.accept(event)

        return user


class UserService:
    def __init__(self, repository: Repository[UserSchema]):
        self.repository: Repository[UserSchema] = repository

    @staticmethod
    def verify_account(email: str, code: str):
        _code = active_codes.get(email)
        if _code:
            active_codes.pop(email)
        return _code == code

    async def get_user(
        self, *, user_id: Optional[int] = None, email: Optional[str] = None
    ) -> UserSchema | None:
        if user_id is not None:
            return await self.repository.get_by_id(user_id)
        return await self.repository.get_one(email=email)

    async def add_user(self, user_create: UserCreate) -> UserSchema:
        user = await self.get_user(email=user_create.email)

        if user is not None:
            raise exceptions.duplicate_user

        return await UserCreatorService(self.repository).create_user(user_create)

    async def verify_user_account(self, email: str, code: str):
        user = await self.get_user(email=email)
        if user is None:
            raise exceptions.user_not_found

        if user.is_verified:
            raise exceptions.user_already_verified

        code_valid = self.verify_account(email, code)
        if not code_valid:
            raise exceptions.user_not_verified

        return await self.repository.update_by_id(user.id, {"is_verified": True})

    async def update_user(self, user_id: int, update: UserUpdate) -> UserSchema:
        data = update.model_dump(exclude_none=True)
        return await self.repository.update_by_id(user_id, data)
