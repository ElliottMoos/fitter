from typing import Optional, List
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from .base import IDModelMixin


class ProductOrderLink(SQLModel, table=True):
    order_id: Optional[int] = Field(
        default=None, foreign_key="order.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )


class Manufacturer(str, Enum):
    Mizuno = "Mizuno"
    Taylormade = "Taylormade"
    Titleist = "Titleist"


class ProductBase(SQLModel):
    name: str
    manufacturer: Manufacturer
    price: float

    class Config:
        use_enum_values = True


class Product(ProductBase, IDModelMixin, table=True):
    orders: List["Order"] = Relationship(
        back_populates="products", link_model=ProductOrderLink
    )


class ProductRead(ProductBase):
    id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str]
    manufacturer: Optional[Manufacturer]
    price: Optional[float]

    class Config:
        use_enum_values = True


class OrderStatus(str, Enum):
    Created = "Created"
    Processing = "Processing"
    Ready = "Ready"


class OrderBase(SQLModel):
    status: OrderStatus
    fitter_id: Optional[int] = Field(default=None, foreign_key="fitter.id")
    fitting_id: Optional[int] = Field(default=None, foreign_key="fitting.id")
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")

    class Config:
        use_enum_values = True


class Order(OrderBase, IDModelMixin, table=True):
    products: List[Product] = Relationship(
        back_populates="orders", link_model=ProductOrderLink
    )


class OrderRead(OrderBase):
    id: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(SQLModel):
    status: Optional[OrderStatus]
    fitter_id: Optional[int]
    fitting_id: Optional[int]
    store_id: Optional[int]
    customer_id: Optional[int]
    address_id: Optional[int]

    class Config:
        use_enum_values = True
