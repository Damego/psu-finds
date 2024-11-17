from fastapi import HTTPException as BaseHTTPException, status

from src.api.enums import ResponseError, ResponseErrorCode


class HTTPException(BaseHTTPException):
    detail: dict

    def __init__(self, status_code: int, detail: ResponseError):
        super().__init__(status_code=status_code, detail=detail.model_dump())


missing_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.MISSING_TOKEN)
)

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.INVALID_USER_CREDENTIALS)
)

duplicate_user = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.USER_ALREADY_EXISTS)
)

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.INVALID_TOKEN)
)

invalid_token_type = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.INVALID_TOKEN_TYPE)
)

expired_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ResponseError(code=ResponseErrorCode.TOKEN_EXPIRED)
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ResponseError(code=ResponseErrorCode.USER_NOT_FOUND)
)

user_already_verified = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.USER_ALREADY_VERIFIED)
)

user_not_verified = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.USER_NOT_VERIFIED)
)

missing_permissions = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail=ResponseError(code=ResponseErrorCode.MISSING_PERMISSIONS)
)

same_email_address = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.SAME_EMAIL_ADDRESS)
)

email_address_already_taken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.EMAIL_ADDRESS_ALREADY_TAKEN)
)

missing_arguments = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=ResponseError(code=ResponseErrorCode.MISSING_ARGUMENTS)
)

not_your_item = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=ResponseError(code=ResponseErrorCode.NOT_YOUR_ITEM)
)

item_does_not_exists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=ResponseError(code=ResponseErrorCode.ITEM_DOES_NOT_EXIST)
)