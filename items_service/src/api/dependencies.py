from typing import Annotated

from fastapi import Cookie, Depends, Header
import aiohttp

from src.api.exceptions import HTTPException
from src.api.user import UserSchema

from ..repositories.item_repository import ItemsRepository
from ..s3.builder import S3ClientBuilder
from ..s3.client import S3Client
from ..services.item_service import ItemsService
from ..settings import settings

s3_client = (
    S3ClientBuilder()
    .set_access_key(settings.S3_ACCESS_KEY)
    .set_secret_key(settings.S3_SECRET_KEY)
    .set_endpoint_url(settings.S3_ENDPOINT)
    .set_bucket_name(settings.S3_BUCKET)
    .build()
)


def get_s3_client() -> S3Client:
    return s3_client


def get_items_service():
    return ItemsService(ItemsRepository())

session: aiohttp.ClientSession | None = None

async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None)
):
    global session
    if session is None:
        session = aiohttp.ClientSession()
        
    headers = {}
    
    if authorization:
        headers["Authorization"] = authorization
        
    cookies = {}
    if access_token:
        cookies = {"access_token": access_token}
    if refresh_token:
        if cookies.get("access_token"):
            cookies["refresh_token"] = refresh_token
        else:
            cookies = {"access_token": access_token}

    async with session.get("http://localhost:8001/users/me", headers=headers, cookies=cookies,
    ) as response:
        user = await response.json()
        print(user)
        return UserSchema(**user)


ItemsServiceDep = Annotated[ItemsService, Depends(get_items_service)]
S3ClientDep = Annotated[S3Client, Depends(get_s3_client)]
ICurrentUser = Annotated[UserSchema, Depends(get_current_user)]