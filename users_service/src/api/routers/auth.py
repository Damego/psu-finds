from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer

from ..auth import TokenTypes
from ...api import auth
from ...api.dependencies import (
    get_current_user,
    get_user_service,
    validate_auth_user,
    validate_user_register, IUserService,
)
from ...models.schemas.auth import Token
from ...models.schemas.users import UserCreate, UserSchema
from ...services.user_service import UserService

__all__ = ("router",)

router = APIRouter(prefix="/auth", tags=["Users"], dependencies=[Depends(HTTPBearer(auto_error=False))])


@router.post("/signup")
async def signup(
    user_create: UserCreate = Depends(validate_user_register),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.add_user(user_create)


@router.post("/verify")
async def verify_account(email: str, code: str, user_service: IUserService):
    await user_service.verify_user_account(email, code)


@router.post("/signin")
async def signin(
    response: Response,
    user: UserSchema = Depends(validate_auth_user)
) -> Token:
    access_token = auth.create_access_token(user.id)
    refresh_token = auth.create_refresh_token(user.id)
    token = Token(
        access_token=access_token["token"],
        refresh_token=refresh_token["token"],
    )

    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=refresh_token["max_age"],
        secure=True,
        samesite="none",
        httponly=True
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=refresh_token["max_age"],
        secure=True,
        samesite="none",
        httponly=True
    )

    return token


@router.post("/refresh", response_model_exclude_none=True)
async def auth_refresh_jwt(
    response: Response,
    user: UserSchema = Depends(get_current_user(TokenTypes.REFRESH)),
) -> Token:
    access_token = auth.create_access_token(user.id)
    token = Token(access_token=access_token["token"])

    response.set_cookie(
        "access_token", token.access_token, max_age=access_token["max_age"]
    )

    return token
