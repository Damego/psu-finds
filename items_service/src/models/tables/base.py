from abc import abstractmethod
from typing import Annotated

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_128 = Annotated[str, 128]


class BaseTable(DeclarativeBase):
    type_annotation_map = {str_128: String(128)}

    @abstractmethod
    def to_schema_model(self, **kwargs: bool) -> BaseModel:
        raise NotImplementedError

    def __repr__(self):
        kv = " ".join([
            f"{key}={getattr(self, key, None)}"
            for key in self.__table__.columns.keys()
        ])
        return f"<{self.__class__.__name__} {kv}>"
