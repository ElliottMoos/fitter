from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import get_fitter_from_session_token
from app.db.repositories.customer import CustomerRepository
from app.db.repositories.address import AddressRepository
from app.models import State, CustomerUpdate, AddressUpdate, FitterRead


customer_update_router = APIRouter(prefix="/update-customer", tags=["customer-update"])
templates = Jinja2Templates(directory="app/server/templates")


@customer_update_router.get(
    "/{customer_id}", name="customer-update:update-customer-page"
)
async def update_customer_page(
    *,
    customer_id: int,
    request: Request,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    customer = customer_repo.get_customer_by_id(customer_id=customer_id)
    if active_fitter:
        if customer:
            return templates.TemplateResponse(
                "update-customer.html",
                {
                    "title": "Fittr - Update Customer",
                    "request": request,
                    "active_fitter": active_fitter,
                    "states": list(
                        map(lambda state: state.value, State._member_map_.values())
                    ),
                    "customer": customer,
                },
            )
        return RedirectResponse("/customers")
    return RedirectResponse("/login")


@customer_update_router.post(
    "/{customer_id}", name="customer-update:update-customer-page-form"
)
async def update_customer_page_form(
    *,
    customer_id: int,
    address_id: int = Form(...),
    customer_update: CustomerUpdate = Depends(CustomerUpdate.as_form),
    address_update: AddressUpdate = Depends(AddressUpdate.as_form),
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    customer = customer_repo.get_customer_by_id(customer_id=customer_id)
    if active_fitter:
        if customer:
            address_repo.update_address(
                address_update=address_update, address_id=address_id
            )
            customer_repo.update_customer(
                customer_update=customer_update, customer_id=customer_id
            )
            return RedirectResponse(f"/customers/{customer.id}", status_code=303)
        return RedirectResponse("/customers", status_code=303)
    return RedirectResponse("/login")
