from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import lead_fitter
from app.db.repositories.store import StoreRepository
from app.db.repositories.address import AddressRepository
from app.models import State, StoreCreate, AddressCreate, FitterRead, Role


store_create_router = APIRouter(prefix="/create-store", tags=["store-create"])
templates = Jinja2Templates(directory="app/server/templates")


@store_create_router.get("", name="store-create:create-store-page")
async def create_store_page(
    *,
    request: Request,
    lead_fitter: FitterRead = Depends(lead_fitter),
):
    return templates.TemplateResponse(
        "create-store.html",
        {
            "title": "Fittr - Create Store",
            "request": request,
            "active_fitter": lead_fitter,
            "states": list(map(lambda state: state.value, State._member_map_.values())),
        },
    )


@store_create_router.post(
    "", name="store-create:create-store-page-form", dependencies=[Depends(lead_fitter)]
)
async def create_store_page_form(
    *,
    store_create: StoreCreate = Depends(StoreCreate.as_form),
    address_create: AddressCreate = Depends(AddressCreate.as_form),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
):
    db_address = address_repo.create_address(address_create=address_create)
    store_create.address_id = db_address.id
    store_repo.create_store(store_create=store_create)
    return RedirectResponse("/stores", status_code=303)
