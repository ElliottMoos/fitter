from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Fitting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start: datetime
    end: datetime
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    fitter_id: Optional[int] = Field(default=None, foreign_key="fitter.id")
