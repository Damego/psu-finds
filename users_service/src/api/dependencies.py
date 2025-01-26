from typing import Annotated

from fastapi import Cookie, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import email_validator

from src.api.enums import ResponseError, ResponseErrorCode

from .auth import TokenData, TokenTypes
from ..api import auth, exceptions
from ..models.enums import UserPermissions
from ..models.schemas.users import UserCreate, UserSchema
from ..repositories.email_sender_repository import RuSenderStrategy
from ..services.send_email_service import EmailService
from ..services.user_service import UserService
from ..repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin", auto_error=False)


def get_user_service():
    return UserService(UserRepository())


def get_email_service():
    return EmailService(RuSenderStrategy())


def get_current_token_data(
    token: str = Depends(oauth2_scheme),
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None),
):
    _token = token or access_token or refresh_token

    if not _token:
        raise exceptions.missing_token

    try:
        return auth.decode_access_token(_token)
    except ExpiredSignatureError:
        raise exceptions.expired_token
    except InvalidTokenError:
        raise exceptions.invalid_token


def get_current_user(token_type: TokenTypes = TokenTypes.ACCESS):
    async def wrapper(
        service: UserService = Depends(get_user_service),
        token: TokenData = Depends(get_current_token_data),
    ):
        if token["type"] != token_type:
            raise exceptions.invalid_token_type
        return await service.get_user(user_id=token["sub"]["user_id"])

    return wrapper


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user(email=email)

    if not user:
        raise exceptions.invalid_credentials
    if not auth.verify_password_hash(password, user.hashed_password):
        raise exceptions.invalid_credentials
    # if not user.is_verified:
    #     raise exceptions.user_not_verified

    return user


async def validate_user_register(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user(email=email)
    if user is not None:
        raise exceptions.duplicate_user
    
    try:
        email_validator.validate_email(email)
    except email_validator.EmailSyntaxError:
        raise exceptions.HTTPException(401, ResponseError(code=ResponseErrorCode.EMAIL_INCORRECT))

    return UserCreate(name=name, email=email, password=password)


async def validate_user_create(
    name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    permissions: UserPermissions = Form(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user(email=email)
    if user is not None:
        raise exceptions.invalid_credentials

    return UserCreate(
        name=name, email=email, password=password, permissions=permissions
    )


IUserService = Annotated[UserService, Depends(get_user_service)]
ICurrentUser = Annotated[UserSchema, Depends(get_current_user(TokenTypes.ACCESS))]


async def get_admin_user(user: ICurrentUser):
    if not user.is_admin:
        raise exceptions.missing_permissions

    return user


IAdminUser = Annotated[UserSchema, Depends(get_admin_user)]
