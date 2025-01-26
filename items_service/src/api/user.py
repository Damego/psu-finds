from pydantic import BaseModel, Field

from .enums import UserPermissions

class BaseUser(BaseModel):
    name: str
    email: str
    is_verified: bool = Field(default=False)
    permissions: UserPermissions = Field(default=UserPermissions(0))


class UserSchema(BaseUser):
    id: int

    @property
    def is_admin(self):
        return UserPermissions.ADMINISTRATOR in self.permissions
