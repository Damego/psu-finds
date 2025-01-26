from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from src.models.enums import UserPermissions


class BaseUser(BaseModel):
    name: str
    email: str
    is_verified: bool = Field(default=False)
    permissions: UserPermissions = Field(default=UserPermissions(0))


class UserSchema(BaseUser):
    id: int
    hashed_password: bytes

    @property
    def is_admin(self):
        return UserPermissions.ADMINISTRATOR in self.permissions


class UserCreate(BaseUser):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    hashed_password: Optional[bytes] = Field(default=None)
    is_verified: Optional[bool] = Field(default=None)
    permissions: Optional[UserPermissions] = Field(default=None)
