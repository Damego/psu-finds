from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import BaseTable


class ItemImages(BaseTable):
    __tablename__ = 'item_images'

    item_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    url: Mapped[str]

    def to_schema_model(self):
        return self.url
