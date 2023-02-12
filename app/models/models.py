import re
import random
from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import EmailStr, validator
from sqlmodel import SQLModel, Relationship, Field

from .base import IDModelMixin


class State(str, Enum):
    AL = "AL"
    AK = "AK"
    AZ = "AZ"
    AR = "AR"
    AS = "AS"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DE = "DE"
    DC = "DC"
    FL = "FL"
    GA = "GA"
    GU = "GU"
    HI = "HI"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    IA = "IA"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    ME = "ME"
    MD = "MD"
    MA = "MA"
    MI = "MI"
    MN = "MN"
    MS = "MS"
    MO = "MO"
    MT = "MT"
    NE = "NE"
    NV = "NV"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NY = "NY"
    NC = "NC"
    ND = "ND"
    MP = "MP"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    PR = "PR"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    TT = "TT"
    UT = "UT"
    VT = "VT"
    VA = "VA"
    VI = "VI"
    WA = "WA"
    WV = "WV"
    WI = "WI"
    WY = "WY"


class AddressBase(SQLModel):
    street: str
    street_2: Optional[str] = Field(default="")
    city: str
    state: State
    zip_code: int

    class Config:
        use_enum_values = True


class Address(AddressBase, IDModelMixin, table=True):
    customers: List["Customer"] = Relationship(back_populates="address")
    fitters: List["Fitter"] = Relationship(back_populates="address")
    stores: List["Store"] = Relationship(back_populates="address")


class AddressRead(AddressBase):
    id: int


class AddressCreate(AddressBase):
    pass


class AddressUpdate(SQLModel):
    street: Optional[str]
    street_2: Optional[str]
    city: Optional[str]
    state: Optional[State]
    zip_code: Optional[str]

    class Config:
        use_enum_values = True


class CustomerBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")

    @validator("phone")
    def validate_phone_number(cls, v):
        patterns = (r"\(\w{3}\) \w{3}\-\w{4}", r"^\w{3}\-\w{4}$")
        if not [re.search(pattern, v) for pattern in patterns]:
            raise ValueError("Invalid phone number format.")
        return v


class Customer(CustomerBase, IDModelMixin, table=True):
    address: Optional[Address] = Relationship(back_populates="customers")
    fittings: List["Fitting"] = Relationship(back_populates="customer")


class CustomerRead(CustomerBase):
    id: int


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(SQLModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address_id: Optional[int]


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
    bio: str
    role: Role
    calendar_color: str = Field(default_factory=random_hex_color)
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")

    class Config:
        use_enum_values = True


class Fitter(FitterBase, IDModelMixin, table=True):
    fittings: List["Fitting"] = Relationship(back_populates="fitter")
    store: Optional["Store"] = Relationship(back_populates="fitters")
    address: Optional[Address] = Relationship(back_populates="fitters")


class FitterRead(FitterBase):
    id: int


class FitterCreate(FitterBase):
    pass


class FitterUpdate(SQLModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    role: Optional[Role]
    store_id: Optional[int]
    address_id: Optional[int]

    class Config:
        use_enum_values = True


class FittingBase(SQLModel):
    start: datetime
    end: datetime
    text: str
    barColor: str
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    store_id: Optional[int] = Field(default=None, foreign_key="store.id")
    fitter_id: Optional[int] = Field(default=None, foreign_key="fitter.id")


class Fitting(FittingBase, IDModelMixin, table=True):
    customer: Optional[Customer] = Relationship(back_populates="fittings")
    store: Optional["Store"] = Relationship(back_populates="fittings")
    fitter: Optional[Fitter] = Relationship(back_populates="fittings")


class FittingRead(FittingBase):
    id: int


class FittingCreate(FittingBase):
    pass


class FittingUpdate(SQLModel):
    start: Optional[datetime]
    end: Optional[datetime]
    text: Optional[str]
    barColor: Optional[str]
    customer_id: Optional[int]
    store_id: Optional[int]
    fitter_id: Optional[int]


class StoreBase(SQLModel):
    name: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")


class Store(StoreBase, IDModelMixin, table=True):
    address: Optional[Address] = Relationship(back_populates="stores")
    fitters: List[Fitter] = Relationship(back_populates="store")
    fittings: List[Fitting] = Relationship(back_populates="store")


class StoreRead(StoreBase):
    id: int


class StoreCreate(StoreBase):
    pass


class StoreUpdate(SQLModel):
    name: Optional[str]
    address_id: Optional[int]


class StoreReadAllRelations(StoreRead):
    address: Optional[AddressRead] = None
    fitters: List[FitterRead] = []


class AddressReadAllRelations(AddressRead):
    customers: List[CustomerRead] = []
    fitters: List[FitterRead] = []
    stores: List[StoreRead] = []


class FittingReadFitterDetail(FittingRead):
    customer: Optional[CustomerRead] = None
    store: Optional[StoreRead] = None


class FittingReadCustomerDetail(FittingRead):
    fitter: Optional[FitterRead] = None
    store: Optional[StoreRead] = None


class FittingReadAllRelations(FittingReadFitterDetail):
    fitter: Optional[FitterRead] = None


class FitterReadAllRelations(FitterRead):
    fittings: List[FittingReadFitterDetail] = []
    store: Optional[StoreRead] = None
    address: Optional[AddressRead] = None


class CustomerReadAllRelations(CustomerRead):
    address: Optional[AddressRead] = None
    fittings: List[FittingReadCustomerDetail] = []
