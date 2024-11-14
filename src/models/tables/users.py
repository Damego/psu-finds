from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects import postgresql

from src.database.base import BaseTable, int_pk, str_128
from src.models.enums import UserPermissions
from src.models.schemas.users import UserSchema


class UserTable(BaseTable):
    __tablename__ = "users"

    id: Mapped[int_pk]
    name: Mapped[str_128]
    email: Mapped[str_128]
    hashed_password: Mapped[bytes]
    permissions: Mapped[UserPermissions] = mapped_column(
        postgresql.ENUM(UserPermissions)
    )
    is_verified: Mapped[bool] = mapped_column(default=False)

    def to_schema_model(self):
        return UserSchema(
            id=self.id,
            name=self.name,
            email=self.email,
            hashed_password=self.hashed_password,
            permissions=self.permissions,
            is_verified=self.is_verified,
        )
