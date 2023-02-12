import math
from typing import Callable, List, Optional, TypeVar, Generic, Type

from sqlmodel import SQLModel
from pydantic import BaseModel, root_validator
from fastapi import Query, Depends

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    page: int
    size: int
    pages: int
    items: List[T]
    total: Optional[int]

    @root_validator(pre=True)
    def calc_total(cls, values):
        items = values.get("items")
        total = len(items)
        values.update({"total": total})
        return values


class Paginator(BaseModel, Generic[T]):
    page: int
    size: int

    def paginate(self, records: List[T]) -> Page[T]:
        pages = math.ceil(len(records) / self.size)
        chunks = [
            records[chunk : chunk + self.size]
            for chunk in range(0, len(records), self.size)
        ]
        items = chunks[self.page - 1]
        return Page[T](page=self.page, size=self.size, pages=pages, items=items)


class PaginationQueryParams(BaseModel):
    page: int = Query(default=1, ge=1)
    size: int = Query(default=10, ge=1, le=100)


def get_paginator(model_type: Type[SQLModel]) -> Callable:
    def paginator(params: PaginationQueryParams = Depends()) -> Paginator[model_type]:
        return Paginator[model_type](page=params.page, size=params.size)

    return paginator
