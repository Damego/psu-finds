from ..models.tables.items import ItemTable
from ..repositories.db_repository import SQLAlchemyRepository

class ItemsRepository(SQLAlchemyRepository):
    table_model = ItemTable
