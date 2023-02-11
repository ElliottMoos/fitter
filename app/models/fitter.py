import random
from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel

from .base import IDModelMixin


def random_hex_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


class Role(str, Enum):
    Lead = "Lead"
    Expert = "Expert"
    Apprentice = "Apprentice"


class FitterBase(SQLModel):
    username: str = Field(unique=True)
    password: str
    first_name: str
    last_name: str
    role: Role
    calendar_color: str = Field(default_factory=random_hex_color)
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")

    class Config:
        use_enum_values = True


class Fitter(FitterBase, IDModelMixin, table=True):
    pass


class FitterRead(FitterBase):
    id: int


class FitterCreate(FitterBase):
    pass


class FitterUpdate(SQLModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[Role]
    store_id: Optional[int]
    address_id: Optional[int]

    class Config:
        use_enum_values = True
