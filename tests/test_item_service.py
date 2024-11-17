import pytest

from src.api.dependencies import get_items_service
from src.api.enums import ResponseErrorCode
from src.api.exceptions import HTTPException
from src.models.enums import ItemTypes, ItemStatus
from src.models.schemas.items import CreateItemSchema, UpdateItemSchema
from src.models.schemas.users import UserSchema
from tests.conftest import Storage


@pytest.fixture(scope="session")
def items_service():
    return get_items_service()


@pytest.mark.order(after="test_user_service.py")
class TestItemService:
    @pytest.mark.parametrize(
        "name, type, description",
        [
            ("Студенческий", ItemTypes.LOST, "Потерял студенческий в 5м корпусе"),
            ("Компьютерная мышь Razor", ItemTypes.FOUND, "Нашёл в 8м корпусе 401 аудитории. Оставил там же"),
            ("Билет в театр", ItemTypes.LOST, "Потерял билет в театр на Щелкунчика"),
        ]
    )
    @pytest.mark.asyncio(loop_scope="session")
    async def test_add_item(self, items_service, name, type, description):
        create_item = CreateItemSchema(
            name=name,
            type=type,
            description=description,
        )
        item = await items_service.add_item(create_item, Storage.user)

        assert item.name == name
        assert item.type == type
        assert item.description == description
        assert item.id is not None
        assert item.created_at is not None
        assert item.status == ItemStatus.ACTIVE

        Storage.item = item

    @pytest.mark.asyncio(loop_scope="session")
    async def test_update_item(self, items_service):
        item = (await items_service.get_items())[0]
        new_item_name = f"[Закрыто] {item.name}"
        new_item_description = f"[Закрыто] {item.description}]"
        item_update = UpdateItemSchema(
            name=new_item_name,
            description=new_item_description,
            status=ItemStatus.CLOSED,
        )
        db_item = await items_service.update_item(Storage.user, item.id, item_update)
        assert db_item.name == new_item_name
        assert db_item.description == new_item_description
        assert db_item.status == ItemStatus.CLOSED

    @pytest.mark.asyncio(loop_scope="session")
    async def test_update_item_not_owner(self, items_service):
        other_user = UserSchema(**Storage.user.model_dump(exclude={"id"}), id=0)
        item = Storage.item
        item_update = UpdateItemSchema(
            name=f"[Закрыто] {item.name}",
            description=f"[Закрыто] {item.description}]",
            status=ItemStatus.CLOSED,
        )

        with pytest.raises(HTTPException) as exp:
            await items_service.update_item(other_user, item.id, item_update)
        assert exp.value.detail["code"] == ResponseErrorCode.NOT_YOUR_ITEM

        item_db = await items_service.get_item_by_id(item.id)

        assert item_db.name == item.name
        assert item_db.name != item_update.name

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_item(self, items_service):
        item = Storage.item
        item_db = await items_service.get_item_by_id(item.id)

        assert item_db is not None
        assert item.id == item_db.id
        assert item.name == item_db.name
        assert item.type == item_db.type
        assert item.description == item_db.description
        assert item.created_at == item_db.created_at
        assert item.status == item_db.status

    @pytest.mark.asyncio(loop_scope="session")
    async def test_delete_item(self, items_service):
        item = Storage.item
        user = Storage.user

        await items_service.delete_item(user, item.id)

        with pytest.raises(HTTPException) as exp:
            await items_service.get_item_by_id(item.id)
        assert exp.value.detail["code"] == ResponseErrorCode.ITEM_DOES_NOT_EXIST

    @pytest.mark.asyncio(loop_scope="session")
    async def test_delete_item_which_does_not_exist(self, items_service):
        item = Storage.item
        user = Storage.user
        with pytest.raises(HTTPException) as exp:
            await items_service.delete_item(user, item.id)
        assert exp.value.detail["code"] == ResponseErrorCode.ITEM_DOES_NOT_EXIST

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_item_which_does_not_exist(self, items_service):
        FAKE_ITEM_ID = 0

        with pytest.raises(HTTPException) as exp:
            await items_service.get_item_by_id(FAKE_ITEM_ID)
        assert exp.value.detail["code"] == ResponseErrorCode.ITEM_DOES_NOT_EXIST
