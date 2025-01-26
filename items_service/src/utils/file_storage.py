from uuid import uuid4

import aiofiles
import aiofiles.os
from fastapi import UploadFile

from src.settings import settings


class LocalFileStorage:
    @staticmethod
    async def upload_file(file: UploadFile) -> str:
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid4()}.{file_ext}"
        path = settings.FILES_DIR / filename
        async with aiofiles.open(path, mode="wb") as filehandle:
            await filehandle.write(await file.read())

        return filename

    @staticmethod
    async def delete_file(filename: str):
        await aiofiles.os.remove(settings.FILES_DIR / filename)

    @staticmethod
    async def get_file_path(file: str) -> str:
        return settings.FILES_DIR / file