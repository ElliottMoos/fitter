from typing import Optional, List
from pydantic import root_validator
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from .product import Product
from .product_order_link import ProductOrderLink


class OrderStatus(str, Enum):
    Created = "Created"
    Processing = "Processing"
    Ready = "Ready"


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: OrderStatus
    total: Optional[float]
    fitter_id: Optional[int] = Field(default=None, foreign_key="fitter.id")
    fitting_id: Optional[int] = Field(default=None, foreign_key="fitting.id")
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")
    products: List[Product] = Relationship(
        back_populates="orders", link_model=ProductOrderLink
    )

    @root_validator
    def calculate_total(cls, values):
        values["total"] = sum(product.price for product in values["products"])
        return values

    class Config:
        use_enum_values = True
