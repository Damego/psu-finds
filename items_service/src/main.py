import json
import os
import sys
from typing import Annotated

from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.api.dependencies import ItemsServiceDep, ICurrentUser, S3ClientDep
from src.models.schemas.items import CreateItemSchema, UpdateItemSchema
from src.utils.file_storage import LocalFileStorage

sys.path.insert(1, os.path.join(sys.path[0], ".."))


app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/items/me")
async def get_current_user_items(user: ICurrentUser, service: ItemsServiceDep):
    """Получение всех предметов текущего пользователя"""
    return await service.get_user_items(user.id)


@app.get("/items/{item_id}")
async def get_item(item_id: int, service: ItemsServiceDep):
    """Получение предмета по его уникальному идентификатору"""
    return await service.get_item_by_id(item_id)


@app.patch("/items/{item_id}")
async def update_item(
        item_id: int, item: UpdateItemSchema, user: ICurrentUser, service: ItemsServiceDep
):
    """Обновление предмета по его уникальному идентификатору"""
    return await service.update_item(user, item_id, item)


@app.post("/items/{item_id}")
async def close_item(item_id: int, user: ICurrentUser, service: ItemsServiceDep):
    """Закрывает предмет"""
    return await service.close_item(user, item_id)


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, user: ICurrentUser, service: ItemsServiceDep):
    """Удаление предмета по его уникальному идентификатору"""
    await service.delete_item(user, item_id)


@app.get("/items")
async def get_all_items(service: ItemsServiceDep):
    """
    Получение списка всех предметов
    """
    return await service.get_items()


@app.post("/items")
async def add_item(file: UploadFile, json_payload: Annotated[str, Form()], user: ICurrentUser, service: ItemsServiceDep, s3_client: S3ClientDep):
    """
    Добавление нового предмета
    """
    item = CreateItemSchema(**json.loads(json_payload))
    return await service.add_item(item, file, user)


@app.get("/files/{name}")
async def get_file(name: str):
    return FileResponse(await LocalFileStorage.get_file_path(name))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
)
