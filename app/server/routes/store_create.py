from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import get_fitter_from_session_token
from app.db.repositories.store import StoreRepository
from app.db.repositories.address import AddressRepository
from app.models import State, StoreCreate, AddressCreate, FitterRead


store_create_router = APIRouter(prefix="/create-store", tags=["store-create"])
templates = Jinja2Templates(directory="app/server/templates")


@store_create_router.get("", name="store-create:create-store-page")
async def create_store_page(
    *,
    request: Request,
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        return templates.TemplateResponse(
            "create-store.html",
            {
                "title": "Fittr - Create Store",
                "request": request,
                "active_fitter": active_fitter,
                "states": list(
                    map(lambda state: state.value, State._member_map_.values())
                ),
            },
        )
    return RedirectResponse("/login")


@store_create_router.post("", name="store-create:create-store-page-form")
async def create_store_page_form(
    *,
    store_create: StoreCreate = Depends(StoreCreate.as_form),
    address_create: AddressCreate = Depends(AddressCreate.as_form),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        db_address = address_repo.create_address(address_create=address_create)
        store_create.address_id = db_address.id
        store_repo.create_store(store_create=store_create)
        return RedirectResponse("/stores", status_code=303)
    return RedirectResponse("/login")
