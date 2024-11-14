from ..models.tables.users import UserTable
from src.utils.abstract.db_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    table_model = UserTable
