from typing import Optional

from pydantic import BaseModel, Field

from .client import S3Client


class S3ClientBuilderData(BaseModel):
    endpoint_url: Optional[str] = Field(default=None)
    access_key: Optional[str] = Field(default=None)
    secret_key: Optional[str] = Field(default=None)
    bucket_name: Optional[str] = Field(default=None)


class S3ClientBuilder:
    __data: S3ClientBuilderData

    def __init__(self, data: S3ClientBuilderData):
        self.__data = data

    def set_endpoint_url(self, endpoint_url: str):
        if not endpoint_url:
            raise ValueError("endpoint_url cannot be empty")
        if not endpoint_url.startswith("https://") or len(endpoint_url.split(".")) < 2:
            raise ValueError("Invalid endpoint_url")

        self.__data.endpoint_url = endpoint_url

    def set_access_key(self, access_key: str):
        if not access_key:
            raise ValueError("access_key cannot be empty")
        self.__data.access_key = access_key

    def set_secret_key(self, secret_key: str):
        if not secret_key:
            raise ValueError("secret_key cannot be empty")
        self.__data.secret_key = secret_key

    def set_bucket_name(self, bucket_name: str):
        if not bucket_name:
            raise ValueError("bucket_name cannot be empty")
        self.__data.bucket_name = bucket_name

    def build(self):
        if not self.__data.endpoint_url:
            raise ValueError("endpoint_url was not set")
        if not self.__data.access_key:
            raise ValueError("access_key was not set")
        if not self.__data.secret_key:
            raise ValueError("secret_key was not set")
        if not self.__data.bucket_name:
            raise ValueError("bucket_name was not set")

        return S3Client(
            self.__data.endpoint_url,
            self.__data.access_key,
            self.__data.secret_key,
            self.__data.bucket_name
        )
