from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.config import Config


class S3Client:
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, bucket_name: str):
        self.__endpoint_url = endpoint_url
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__bucket_name = bucket_name

        self._session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self._session.create_client(
            "s3",
            aws_access_key_id=self.__access_key,
            aws_secret_access_key=self.__secret_key,
            endpoint_url=self.__endpoint_url,
            config=Config(s3={"addressing_style": "virtual"}),
        ) as client:
            yield client

    async def upload_file(self, file: bytes, filename: str):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.__bucket_name,
                Body=file,
                Key=filename,
            )
