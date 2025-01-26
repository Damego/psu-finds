from fastapi import HTTPException as BaseHTTPException, status

from ..api.enums import ResponseError, ResponseErrorCode


class HTTPException(BaseHTTPException):
    detail: dict

    def __init__(self, status_code: int, detail: ResponseError):
        super().__init__(status_code=status_code, detail=detail.model_dump())


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