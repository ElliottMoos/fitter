from typing import Optional
from sqlmodel import Field, SQLModel

from .base import IDModelMixin


class StoreBase(SQLModel):
    name: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")


class Store(StoreBase, IDModelMixin, table=True):
    pass


class StoreRead(StoreBase):
    id: int


class StoreCreate(StoreBase):
    pass


class StoreUpdate(SQLModel):
    name: Optional[str]
    address_id: Optional[int]
