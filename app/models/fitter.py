from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel


class Role(str, Enum):
    Lead = "Lead"
    Expert = "Expert"
    Apprentice = "Apprentice"


class Fitter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    role: Role
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")

    class Config:
        use_enum_values = True
