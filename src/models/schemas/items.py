from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.models.enums import ItemTypes, ItemStatus


class CreateItemSchema(BaseModel):
    name: str
    type: ItemTypes
    description: str


class ItemSchema(BaseModel):
    id: int
    user_id: int
    name: str
    type: ItemTypes
    created_at: datetime
    description: str
    status: ItemStatus


class UpdateItemSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    type: Optional[ItemTypes] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status: Optional[ItemStatus] = Field(default=None)
