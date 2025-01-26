from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from ...api.dependencies import (
    get_current_user,
    get_user_service,
    IAdminUser,
    validate_user_create,
)
from ...models.schemas.users import BaseUser, UserCreate, UserSchema, UserUpdate
from ...services.user_service import UserService
from .. import exceptions

__all__ = ("router",)

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(HTTPBearer(auto_error=False))])


@router.post("")
async def create_user(
    admin_user: IAdminUser,
    user_create: UserCreate = Depends(validate_user_create),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.add_user(user_create)
    return user


@router.get("/me", response_model_exclude={"hashed_password"})
async def get_me(user: UserSchema = Depends(get_current_user())) -> UserSchema:
    return user


@router.patch("/me")
async def change_user_name(
    name: str,
    user: UserSchema = Depends(get_current_user()),
    user_service: UserService = Depends(get_user_service)
):
    if not name:
        raise exceptions.missing_arguments

    await user_service.update_user(user.id, UserUpdate(name=name))


@router.get("/{user_id}")
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user(user_id=user_id)
