from typing import Optional
from sqlmodel import Field, SQLModel


class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")
