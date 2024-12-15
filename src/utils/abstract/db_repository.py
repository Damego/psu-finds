from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Unpack

from pydantic import BaseModel
from sqlalchemy import insert, select, delete, update
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.orm import selectinload, load_only

from src.database.base import BaseTable
from src.database.session import async_session_maker
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
    table_model: Type[BaseTable] = None
    options: list[ExecutableOption] = []

    def __insert_query_options(self, query, options: Optional[list[ExecutableOption]] = None):
        for option in self.options:
            query = query.options(option)
        if options:
            for option in options:
                query = query.options(option)
        return query

    async def get_by_id(self, id: int, relationship: list[Any] = None):
        return await self.get_one(id=id)

    async def get_one(
        self, *relationship: Optional[Any], **filter: Unpack[table_model]
    ) -> BaseModel | None:
        async with async_session_maker() as session:
            query = select(self.table_model).filter_by(**dict_filter_none(filter))
            if relationship:
                query.options(selectinload(*relationship))
            query = self.__insert_query_options(query)

            result = await session.execute(query)
            data = result.scalar_one_or_none()
            return data.to_schema_model() if data else None

    async def get_many(
        self, options: list[ExecutableOption] = None, **filter: Unpack[table_model]
    ) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.table_model).filter_by(**dict_filter_none(filter))
            query = self.__insert_query_options(query, options)

            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

    async def add_one(self, data: dict) -> table_model:
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

    async def get_all(self, relationships: Optional[list[Any]] = None, load_attr: Optional[list[Any]] = None) -> list[BaseModel]:
        async with async_session_maker() as session:
            query = select(self.table_model)
            if relationships:
                load = selectinload(*relationships)
                if load_attr:
                    load.load_only(*load_attr)
                query.options(load)
            query = self.__insert_query_options(query)

            result = await session.execute(query)
            return [table.to_schema_model() for table in result.scalars().all()]

    async def update_by_id(self, id: int, data: dict[str, Any]) -> None:
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
