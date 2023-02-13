from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import get_fitter_from_session_token
from app.db.repositories.store import StoreRepository
from app.db.repositories.address import AddressRepository
from app.models import State, StoreUpdate, AddressUpdate, FitterRead


store_update_router = APIRouter(prefix="/update-store", tags=["store-update"])
templates = Jinja2Templates(directory="app/server/templates")


@store_update_router.get("/{store_id}", name="store-update:update-store-page")
async def update_store_page(
    *,
    store_id: int,
    request: Request,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    store = store_repo.get_store_by_id(store_id=store_id)
    if active_fitter:
        if store:
            return templates.TemplateResponse(
                "update-store.html",
                {
                    "title": "Fittr - Update Store",
                    "request": request,
                    "active_fitter": active_fitter,
                    "states": list(
                        map(lambda state: state.value, State._member_map_.values())
                    ),
                    "store": store,
                },
            )
    return RedirectResponse("/login")


@store_update_router.post("/{store_id}", name="store-update:update-store-page-form")
async def update_store_page_form(
    *,
    store_id: int,
    address_id: int = Form(...),
    store_update: StoreUpdate = Depends(StoreUpdate.as_form),
    address_update: AddressUpdate = Depends(AddressUpdate.as_form),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    store = store_repo.get_store_by_id(store_id=store_id)
    if active_fitter:
        if store:
            store_repo.update_store(store_update=store_update, store_id=store_id)
            address_repo.update_address(
                address_update=address_update, address_id=address_id
            )
            return RedirectResponse(f"/stores/{store.id}", status_code=303)
    return RedirectResponse("/login")
