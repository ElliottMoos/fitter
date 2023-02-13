from typing import List, Optional
from fastapi import Depends, APIRouter, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.server.dependencies.auth import get_fitter_from_session_token
from app.server.dependencies.database import get_repository
from app.server.dependencies.pagination import Page, Paginator, get_paginator
from app.models import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
    CustomerReadAllRelations,
)
from app.models import FitterRead, State
from app.db.repositories.customer import CustomerRepository


customers_api_router = APIRouter(prefix="/customers", tags=["customers"])
customers_template_router = APIRouter(prefix="/customers", tags=["customers"])
templates = Jinja2Templates(directory="app/server/templates")


@customers_api_router.get(
    "",
    response_model=List[CustomerRead],
    name="customers:get-customers",
)
async def get_customers(
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> List[CustomerRead]:
    return customer_repo.get_all_customers()


@customers_api_router.post(
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


@customers_api_router.get(
    "/{customer_id}",
    response_model=CustomerReadAllRelations,
    name="customers:get-customer",
)
async def get_customer(
    *,
    customer_id: int,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerReadAllRelations:
    return customer_repo.get_customer_by_id(customer_id=customer_id)


@customers_api_router.put(
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


@customers_api_router.delete(
    "/{customer_id}",
    response_model=CustomerRead,
    name="customers:delete-customer",
)
async def delete_customer(
    *,
    customer_id: int,
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
) -> CustomerRead:
    return customer_repo.delete_customer(customer_id=customer_id)


@customers_template_router.get("", name="customers:customers-page")
async def customers_page(
    *,
    request: Request,
    first_name: Optional[str] = Query(default=""),
    last_name: Optional[str] = Query(default=""),
    paginator: Paginator[CustomerRead] = Depends(get_paginator(CustomerRead)),
    customer_repo: CustomerRepository = Depends(get_repository(CustomerRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        if first_name or last_name:
            page = paginator.paginate(
                customer_repo.get_customers_name_search(
                    first_name=first_name, last_name=last_name
                )
            )
            return templates.TemplateResponse(
                "customers.html",
                {
                    "title": "Fittr - Customers",
                    "request": request,
                    "page": page,
                    "active_fitter": active_fitter,
                    "first_name_query": f"&first_name={first_name}",
                    "last_name_query": f"&last_name={last_name}",
                },
            )
        page = paginator.paginate(customer_repo.get_all_customers())
        return templates.TemplateResponse(
            "customers.html",
            {
                "title": "Fittr - Customers",
                "request": request,
                "page": page,
                "active_fitter": active_fitter,
            },
        )
    return RedirectResponse("/login")


@customers_template_router.get("/{customer_id}", name="customers:customer-page")
async def customers_page(
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
                "customer.html",
                {
                    "title": "Fittr - Customer",
                    "request": request,
                    "customer": customer,
                    "active_fitter": active_fitter,
                },
            )
    return RedirectResponse("/login")
