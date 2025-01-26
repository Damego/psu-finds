from enum import IntEnum, IntFlag

from pydantic import BaseModel


class ResponseErrorCode(IntEnum):
    # 100XX & 101XX taken by users service

    MISSING_ARGUMENTS = 10200

    NOT_YOUR_ITEM = 10300
    ITEM_DOES_NOT_EXIST = 10301


class ResponseError(BaseModel):
    code: ResponseErrorCode


class UserPermissions(IntFlag):
    NONE = 0
    ADMINISTRATOR = 1 << 0
