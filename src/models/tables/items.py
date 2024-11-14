from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import BaseTable, int_pk, str_128
from src.models.enums import ItemTypes, ItemStatus
from src.models.schemas.items import ItemSchema
from src.models.tables.users import UserTable


class ItemTable(BaseTable):
    __tablename__ = "items"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str_128]
    type: Mapped[ItemTypes] = mapped_column(postgresql.ENUM(ItemTypes))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    description: Mapped[str]
    status: Mapped[ItemStatus] = mapped_column(postgresql.ENUM(ItemStatus))

    user: Mapped[UserTable] = relationship()

    def to_schema_model(self):
        return ItemSchema(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            type=self.type,
            created_at=self.created_at,
            description=self.description,
            status=self.status,
        )
