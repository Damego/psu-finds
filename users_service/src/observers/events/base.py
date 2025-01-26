from pydantic import BaseModel


class BaseEvent[T: BaseModel](BaseModel):
    data: T
