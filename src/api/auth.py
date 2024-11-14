from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import TypedDict

import bcrypt
import jwt

from ..settings import settings


class TokenTypes(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.value
        return super().__eq__(other)


class TokenData(TypedDict):
    type: str
    sub: dict


def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password_hash(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_jwt(*, type: TokenTypes, payload: dict, expire_delta: timedelta) -> str:
    payload = {
        "type": type.value,
        "sub": payload,
        "exp": datetime.now(timezone.utc) + expire_delta,
    }
    return jwt.encode(
        payload, settings.auth_jwt.PRIVATE_KEY, algorithm=settings.auth_jwt.algorithm
    )


def create_access_token(user_id: int):
    # TODO:
    #   Спасибо Remix, что оно такое говно
    max_age = timedelta(days=7)
    return {
        "token": create_jwt(
            type=TokenTypes.ACCESS, payload={"user_id": user_id}, expire_delta=max_age
        ),
        "max_age": max_age,
    }


def create_refresh_token(user_id: int):
    max_age = timedelta(days=30)
    return {
        "token": create_jwt(
            type=TokenTypes.REFRESH, payload={"user_id": user_id}, expire_delta=max_age
        ),
        "max_age": max_age,
    }


def decode_access_token(token: str) -> dict:
    return TokenData(
        **jwt.decode(
            token,
            settings.auth_jwt.PUBLIC_KEY,
            algorithms=[settings.auth_jwt.algorithm],
        )
    )
