from typing import Optional
from sqlmodel import Field, SQLModel


class IDModelMixin(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
