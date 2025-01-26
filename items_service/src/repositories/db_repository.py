from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel
from sqlalchemy import insert, select, delete, update
from sqlalchemy.sql.base import ExecutableOption

from src.database.session import async_session_maker
from src.models.tables.base import BaseTable
from src.utils.filters import dict_filter_none


class Repository[T](ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, **filter: Any) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict) -> T:
        raise NotImplementedError

    @abstractmethod
    async def remove_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, id: int, data: dict[str, Any]) -> T:
        raise NotImplementedError


class SQLAlchemyRepository(Repository):
    table_model: Type[BaseTable] = None # type: ignore
    options: list[ExecutableOption] = []

    async def get_by_id(self, id: int):
        return await self.get_one(id=id)

    async def get_one(
        self,  **filter: Any
    ) -> BaseModel | None:
        async with async_session_maker() as session:
            query = select(self.table_model).filter_by(**dict_filter_none(filter))
            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model() if data else None

    async def get_many(
        self, **filter: dict[str, Any]
    ) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.table_model).filter_by(**dict_filter_none(filter))
            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            result = await session.execute(
                insert(self.table_model).values(**data).returning(self.table_model)
            )
            await session.commit()
            return result.scalar_one().to_schema_model()

    async def add_many(self, data: list[dict]):
        async with async_session_maker() as session:
            await session.execute(
                insert(self.table_model).values(data)
            )
            await session.commit()

    async def remove_by_id(self, id: int):
        async with async_session_maker() as session:
            await session.execute(delete(self.table_model).filter_by(id=id))
            await session.commit()

    async def get_all(self) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.table_model)
            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

    async def update_by_id(self, id: int, data: dict[str, Any]):
        async with async_session_maker() as session:
            query = (
                update(self.table_model)
                .filter_by(id=id)
                .values(**dict_filter_none(data))
                .returning(self.table_model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one().to_schema_model()
