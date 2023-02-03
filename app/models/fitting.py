from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

from .base import IDModelMixin


class FittingBase(SQLModel):
    start: datetime
    end: datetime
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    fitter_id: Optional[int] = Field(default=None, foreign_key="fitter.id")


class Fitting(FittingBase, IDModelMixin, table=True):
    pass


class FittingRead(FittingBase):
    id: int


class FittingCreate(FittingBase):
    pass


class FittingUpdate(SQLModel):
    start: Optional[datetime]
    end: Optional[datetime]
    customer_id: Optional[int]
    store_id: Optional[int]
    fitter_id: Optional[int]
