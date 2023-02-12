from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_fitter_from_session_token
from app.db.repositories.customer import CustomerRepository
from app.db.repositories.address import AddressRepository
from app.models import State, CustomerCreate, AddressCreate, FitterRead


customer_create_router = APIRouter(prefix="/create-customer", tags=["customer-create"])
templates = Jinja2Templates(directory="app/api/templates")


class CreateCustomerParams(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: EmailStr = Form(...),
        phone: str = Form(...),
    ) -> BaseModel:
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )


class CreateAddressParams(BaseModel):
    street: str
    street_2: Optional[str] = ""
    city: str
    state: State
    zip_code: str

    @classmethod
    def as_form(
        cls,
        street: str = Form(...),
        street_2: Optional[str] = Form(default=""),
        city: str = Form(...),
        state: State = Form(...),
        zip_code: str = Form(...),
    ) -> BaseModel:
        return cls(
            street=street,
            street_2=street_2,
            city=city,
            state=state,
            zip_code=zip_code,
        )


@customer_create_router.get("", name="customer-create:create-customer-page")
async def create_customer_page(
    *,
    request: Request,
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        return templates.TemplateResponse(
            "create-customer.html",
            {
                "title": "Fittr - Create Customer",
                "request": request,
                "active_fitter": active_fitter,
                "states": list(
                    map(lambda state: state.value, State._member_map_.values())
                ),
            },
        )
    return RedirectResponse("/login")


@customer_create_router.post("", name="customer-create:create-customer-page-form")
async def create_customer_page_form(
    *,
    customer_params: CreateCustomerParams = Depends(CreateCustomerParams.as_form),
    address_params: CreateAddressParams = Depends(CreateAddressParams.as_form),
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        customer_create = CustomerCreate(**customer_params.dict())
        address_create = AddressCreate(**address_params.dict())
        db_address = address_repo.create_address(address_create=address_create)
        customer_create.address_id = db_address.id
        customer_repo.create_customer(customer_create=customer_create)
        return RedirectResponse("/customers", status_code=303)
    return RedirectResponse("/login")
