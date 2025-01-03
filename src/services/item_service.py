from src.api import exceptions
from src.models.enums import ItemStatus
from src.models.schemas.items import ItemSchema, CreateItemSchema, UpdateItemSchema
from src.models.schemas.users import UserSchema

from src.utils.abstract.db_repository import Repository


class ItemService:
    def __init__(self, repository: Repository[ItemSchema]):
        self.repository: Repository[ItemSchema] = repository

    async def get_item_by_id(self, item_id: int) -> ItemSchema:
        item = await self.repository.get_by_id(item_id)
        if item is None:
            raise exceptions.item_does_not_exists
        return item

    async def get_items(self) -> list[ItemSchema]:
        return await self.repository.get_all()

    async def get_user_items(self, user_id: int) -> list[ItemSchema]:
        return await self.repository.get_many(user_id=user_id)

    async def add_item(self, item: CreateItemSchema, user: UserSchema) -> ItemSchema:
        return await self.repository.add_one({**item.model_dump(), "user_id": user.id, "status": ItemStatus.ACTIVE})

    async def update_item(
        self, user: UserSchema, item_id: int, item_update: UpdateItemSchema
    ) -> ItemSchema | None:
        item = await self.get_item_by_id(item_id)

        if not user.is_admin and item.user_id != user.id:
            raise exceptions.not_your_item

        return await self.repository.update_by_id(item_id, item_update.model_dump())

    async def delete_item(self, user: UserSchema, item_id: int) -> None:
        item = await self.get_item_by_id(item_id)

        if not user.is_admin and item.user_id != user.id:
            raise exceptions.not_your_item

        await self.repository.remove_by_id(item_id)
