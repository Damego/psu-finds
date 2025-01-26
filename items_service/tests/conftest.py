import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database.base import BaseTable
from src.database import session
from src.models.schemas.items import ItemSchema
from src.models.schemas.users import UserSchema
from src.settings import settings


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)

    async with engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.drop_all)
        await conn.run_sync(BaseTable.metadata.create_all)

    session.engine = engine
    session.async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Storage:
    user: UserSchema = None
    item: ItemSchema = None
