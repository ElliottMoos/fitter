from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel


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


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    street: str
    street_2: Optional[str] = Field(default="")
    city: str
    state: State
    zip_code: int

    class Config:
        use_enum_values = True
