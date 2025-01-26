from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTable, int_pk, str_128
from ..enums import ItemTypes, ItemStatus
from ..schemas.items import ItemSchema


class ItemTable(BaseTable):
    __tablename__ = "items"

    id: Mapped[int_pk]
    user_id: Mapped[int]
    name: Mapped[str_128]
    type: Mapped[ItemTypes] = mapped_column(postgresql.ENUM(ItemTypes))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    description: Mapped[str]
    status: Mapped[ItemStatus] = mapped_column(postgresql.ENUM(ItemStatus))
    image_url: Mapped[str_128]

    def to_schema_model(self):
        return ItemSchema(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            type=self.type,
            created_at=self.created_at,
            description=self.description,
            status=self.status,
            image_url=self.image_url,
        )
