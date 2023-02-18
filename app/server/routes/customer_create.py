from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import active_fitter
from app.db.repositories.customer import CustomerRepository
from app.db.repositories.address import AddressRepository
from app.models import State, CustomerCreate, AddressCreate, FitterRead


customer_create_router = APIRouter(prefix="/create-customer", tags=["customer-create"])
templates = Jinja2Templates(directory="app/server/templates")


@customer_create_router.get("", name="customer-create:create-customer-page")
async def create_customer_page(
    *,
    request: Request,
    active_fitter: FitterRead = Depends(active_fitter),
):
    return templates.TemplateResponse(
        "create-customer.html",
        {
            "title": "Fittr - Create Customer",
            "request": request,
            "active_fitter": active_fitter,
            "states": list(map(lambda state: state.value, State._member_map_.values())),
        },
    )


@customer_create_router.post(
    "",
    name="customer-create:create-customer-page-form",
    dependencies=[Depends(active_fitter)],
)
async def create_customer_page_form(
    *,
    customer_create: CustomerCreate = Depends(CustomerCreate.as_form),
    address_create: AddressCreate = Depends(AddressCreate.as_form),
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
):
    db_address = address_repo.create_address(address_create=address_create)
    customer_create.address_id = db_address.id
    customer_repo.create_customer(customer_create=customer_create)
    return RedirectResponse("/customers", status_code=303)
