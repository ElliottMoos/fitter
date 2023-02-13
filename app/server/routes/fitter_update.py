from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from app.services import auth_service
from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import get_fitter_from_session_token
from app.db.repositories.store import StoreRepository
from app.db.repositories.fitter import FitterRepository
from app.db.repositories.address import AddressRepository
from app.models import State, FitterUpdate, AddressUpdate, FitterRead, Role


fitter_update_router = APIRouter(prefix="/update-fitter", tags=["fitter-update"])
templates = Jinja2Templates(directory="app/server/templates")


@fitter_update_router.get("/{fitter_id}", name="fitter-update:update-fitter-page")
async def update_fitter_page(
    *,
    fitter_id: int,
    request: Request,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    fitter = fitter_repo.get_fitter_by_id(fitter_id=fitter_id)
    if active_fitter:
        if fitter:
            return templates.TemplateResponse(
                "update-fitter.html",
                {
                    "title": "Fittr - Update Fitter",
                    "request": request,
                    "active_fitter": active_fitter,
                    "states": list(
                        map(lambda state: state.value, State._member_map_.values())
                    ),
                    "roles": list(
                        map(lambda role: role.value, Role._member_map_.values())
                    ),
                    "fitter": fitter,
                    "stores": store_repo.get_all_stores(),
                },
            )
        return RedirectResponse("/fitters")
    return RedirectResponse("/login")


@fitter_update_router.post("/{fitter_id}", name="fitter-update:update-fitter-page-form")
async def update_fitter_page_form(
    *,
    request: Request,
    fitter_id: int,
    address_id: int = Form(...),
    fitter_update: FitterUpdate = Depends(FitterUpdate.as_form),
    address_update: AddressUpdate = Depends(AddressUpdate.as_form),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    fitter = fitter_repo.get_fitter_by_id(fitter_id=fitter_id)
    if active_fitter:
        if fitter:
            if fitter_update.password:
                fitter_update.password = auth_service.hash_password(
                    password=fitter_update.password
                )
            else:
                fitter_update.password = fitter.password
            try:
                fitter_repo.update_fitter(
                    fitter_update=fitter_update, fitter_id=fitter_id
                )
                address_repo.update_address(
                    address_update=address_update, address_id=address_id
                )
            except IntegrityError:
                stores = store_repo.get_all_stores()
                return templates.TemplateResponse(
                    "update-fitter.html",
                    {
                        "title": "Fittr - Create Fitter",
                        "request": request,
                        "active_fitter": active_fitter,
                        "fitter": fitter,
                        "states": list(
                            map(lambda state: state.value, State._member_map_.values())
                        ),
                        "roles": list(
                            map(lambda role: role.value, Role._member_map_.values())
                        ),
                        "stores": stores,
                        "errors": [
                            f"Username '{fitter_update.username}' already exists"
                        ],
                    },
                )
            return RedirectResponse(f"/fitters/{fitter.id}", status_code=303)
        return RedirectResponse("/fitters", status_code=303)
    return RedirectResponse("/login")
