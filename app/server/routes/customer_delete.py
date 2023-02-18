from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import active_fitter
from app.db.repositories.customer import CustomerRepository


customer_delete_router = APIRouter(prefix="/delete-customer", tags=["customer-delete"])
templates = Jinja2Templates(directory="app/server/templates")


@customer_delete_router.get(
    "/{customer_id}",
    name="customer-delete:delete-customer",
    dependencies=[Depends(active_fitter)],
)
async def delete_customer(
    *,
    customer_id: int,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
):
    customer = customer_repo.get_customer_by_id(customer_id=customer_id)
    if customer:
        customer_repo.delete_customer(customer_id=customer_id)
        return RedirectResponse("/customers")
    raise HTTPException(status_code=404, detail="Customer not found")
