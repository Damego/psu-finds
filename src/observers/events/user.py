from pydantic import BaseModel

from src.models.schemas.users import UserSchema
from src.observers.events.base import BaseEvent


class UserCreatedEventData(BaseModel):
    verification_code: str
    user: UserSchema


UserCreatedEvent = BaseEvent[UserCreatedEventData]
