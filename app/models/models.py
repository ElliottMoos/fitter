import random
from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import EmailStr
from fastapi import Form
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
    @classmethod
    def as_form(
        cls,
        street: str = Form(...),
        street_2: Optional[str] = Form(default=""),
        city: str = Form(...),
        state: State = Form(...),
        zip_code: str = Form(...),
    ) -> SQLModel:
        return cls(
            street=street,
            street_2=street_2,
            city=city,
            state=state,
            zip_code=zip_code,
        )


class AddressUpdate(SQLModel):
    street: Optional[str]
    street_2: Optional[str]
    city: Optional[str]
    state: Optional[State]
    zip_code: Optional[str]

    @classmethod
    def as_form(
        cls,
        street: Optional[str] = Form(default=None),
        street_2: Optional[str] = Form(default=None),
        city: Optional[str] = Form(default=None),
        state: Optional[State] = Form(default=None),
        zip_code: Optional[str] = Form(default=None),
    ) -> SQLModel:
        return cls(
            street=street,
            street_2=street_2,
            city=city,
            state=state,
            zip_code=zip_code,
        )


class CustomerBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")


class Customer(CustomerBase, IDModelMixin, table=True):
    address: Optional[Address] = Relationship(
        back_populates="customers",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )
    fittings: List["Fitting"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class CustomerRead(CustomerBase):
    id: int


class CustomerCreate(CustomerBase):
    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: EmailStr = Form(...),
        phone: str = Form(...),
    ) -> SQLModel:
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )


class CustomerUpdate(SQLModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address_id: Optional[int]

    @classmethod
    def as_form(
        cls,
        first_name: Optional[str] = Form(default=None),
        last_name: Optional[str] = Form(default=None),
        email: Optional[EmailStr] = Form(default=None),
        phone: Optional[str] = Form(default=None),
        address_id: Optional[int] = Form(default=None),
    ) -> SQLModel:
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_id=address_id,
        )


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
    fittings: List["Fitting"] = Relationship(
        back_populates="fitter",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )
    store: Optional["Store"] = Relationship(back_populates="fitters")
    address: Optional[Address] = Relationship(
        back_populates="fitters",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class FitterRead(FitterBase):
    id: int


class FitterCreate(FitterBase):
    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        bio: str = Form(...),
        role: Role = Form(...),
    ) -> SQLModel:
        return cls(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            bio=bio,
            role=role,
        )


class FitterUpdate(SQLModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    role: Optional[Role]
    store_id: Optional[int]
    address_id: Optional[int]

    @classmethod
    def as_form(
        cls,
        username: Optional[str] = Form(default=None),
        password: Optional[str] = Form(default=None),
        first_name: Optional[str] = Form(default=None),
        last_name: Optional[str] = Form(default=None),
        bio: Optional[str] = Form(default=None),
        role: Optional[Role] = Form(default=None),
        store_id: Optional[int] = Form(default=None),
        address_id: Optional[int] = Form(default=None),
    ) -> SQLModel:
        return cls(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            role=role,
            store_id=store_id,
            address_id=address_id,
        )


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
    phone: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")


class Store(StoreBase, IDModelMixin, table=True):
    address: Optional[Address] = Relationship(
        back_populates="stores",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )
    fitters: List[Fitter] = Relationship(back_populates="store")
    fittings: List[Fitting] = Relationship(
        back_populates="store",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class StoreRead(StoreBase):
    id: int


class StoreCreate(StoreBase):
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        phone: str = Form(...),
    ) -> SQLModel:
        return cls(name=name, phone=phone)


class StoreUpdate(SQLModel):
    name: Optional[str]
    phone: Optional[str]
    address_id: Optional[int]

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(default=None),
        phone: Optional[str] = Form(default=None),
        address_id: Optional[int] = Form(default=None),
    ) -> SQLModel:
        return cls(name=name, phone=phone, address_id=address_id)


class StoreReadAllRelations(StoreRead):
    address: Optional[AddressRead] = None
    fitters: List[FitterRead] = []
    fittings: List[FittingRead] = []


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
