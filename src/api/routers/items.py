from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.api.dependencies import ItemServiceDep, ICurrentUser
from src.models.schemas.items import CreateItemSchema, UpdateItemSchema

__all__ = ("router",)

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    dependencies=[Depends(HTTPBearer(auto_error=False))],
)


@router.get("/me")
async def get_current_user_items(user: ICurrentUser, service: ItemServiceDep):
    """Получение всех предметов текущего пользователя"""
    return await service.get_user_items(user.id)


@router.get("/{item_id}")
async def get_item(item_id: int, service: ItemServiceDep):
    """Получение предмета по его уникальному идентификатору"""
    return await service.get_item(item_id)


@router.patch("/{item_id}")
async def update_item(
    item_id: int, item: UpdateItemSchema, user: ICurrentUser, service: ItemServiceDep
):
    """Обновление предмета по его уникальному идентификатору"""
    return await service.update_item(user, item_id, item)


@router.post("/{item_id}")
async def close_item(item_id: int, user: ICurrentUser, service: ItemServiceDep):
    """Закрывает предмет"""
    return await service.close_item(user, item_id)


@router.delete("/{item_id}")
async def delete_item(item_id: int, user: ICurrentUser, service: ItemServiceDep):
    """Удаление предмета по его уникальному идентификатору"""
    await service.delete_item(user, item_id)


@router.get("")
async def get_all_items(service: ItemServiceDep):
    """
    Получение списка всех предметов
    """
    return await service.get_items()


@router.post("")
async def add_item(item: CreateItemSchema, user: ICurrentUser, service: ItemServiceDep):
    """
    Добавление нового предмета
    """
    return await service.add_item(item, user)
