from ..models.tables.items import ItemTable
from src.utils.abstract.db_repository import SQLAlchemyRepository


class ItemRepository(SQLAlchemyRepository):
    table_model = ItemTable
