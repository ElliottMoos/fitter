from typing import List
from fastapi import Depends, APIRouter

from app.api.dependencies.database import get_repository
from app.models.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.db.repositories.customer import CustomerRepository


customers_router = APIRouter(prefix="/customers", tags=["customers"])


@customers_router.get(
    "",
    response_model=List[CustomerRead],
    name="customers:get-customers",
)
async def get_customers(
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> List[CustomerRead]:
    return customer_repo.get_all_customers()


@customers_router.post(
    "",
    response_model=CustomerRead,
    name="customers:create-customer",
)
async def create_customer(
    *,
    customer_create: CustomerCreate,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    return customer_repo.create_customer(customer_create=customer_create)


@customers_router.get(
    "/{customer_id}",
    response_model=CustomerRead,
    name="customers:get-customer",
)
async def get_customer(
    *,
    customer_id: int,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    return customer_repo.get_customer_by_id(customer_id=customer_id)


@customers_router.put(
    "/{customer_id}",
    response_model=CustomerRead,
    name="customers:update-customer",
)
async def update_customer(
    *,
    customer_id: int,
    customer_update: CustomerUpdate,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    return customer_repo.update_customer(
        customer_update=customer_update, customer_id=customer_id
    )
