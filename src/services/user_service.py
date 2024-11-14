from typing import Optional, Type

from ..api import auth
from ..models.schemas.users import UserCreate, UserSchema, UserUpdate
from src.utils.abstract.db_repository import Repository


class UserService:
    def __init__(self, repository_type: Type[Repository]):
        self.repository: Repository = repository_type()

    async def get_users(self) -> list[UserSchema]:
        return await self.repository.get_many()

    async def get_user(
        self, *, user_id: Optional[int] = None, email: Optional[str] = None
    ) -> UserSchema | None:
        if user_id is not None:
            return await self.repository.get_by_id(user_id)
        return await self.repository.get_one(email=email)

    async def add_user(self, user_create: UserCreate) -> UserSchema:
        hashed_password = auth.get_password_hash(user_create.password)
        payload = {
            "name": user_create.name,
            "email": user_create.email,
            "hashed_password": hashed_password,
            "permissions": 0,
            "is_verified": False,
        }
        return await self.repository.add_one(payload)

    async def update_user(self, user_id: int, update: UserUpdate) -> UserSchema:
        data = update.model_dump(exclude_none=True)
        return await self.repository.update_by_id(user_id, data)
