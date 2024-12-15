from pydantic import BaseModel

from src.models.schemas.users import UserSchema


class UserCreatedEvent(BaseModel):
    verification_code: str
    user: UserSchema
