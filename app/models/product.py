from typing import List, Optional
from enum import Enum
from sqlmodel import SQLModel, Relationship, Field
from .order import Order
from .product_order_link import ProductOrderLink


class Manufacturer(str, Enum):
    Mizuno = "Mizuno"
    Taylormade = "Taylormade"
    Titleist = "Titleist"


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    manufacturer: Manufacturer
    price: float
    orders: List[Order] = Relationship(
        back_populates="products", link_model=ProductOrderLink
    )

    class Config:
        use_enum_values = True
