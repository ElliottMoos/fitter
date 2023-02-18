from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from app.services import auth_service
from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import lead_fitter
from app.db.repositories.store import StoreRepository
from app.db.repositories.fitter import FitterRepository
from app.db.repositories.address import AddressRepository
from app.models import State, FitterCreate, AddressCreate, FitterRead, Role


fitter_create_router = APIRouter(prefix="/create-fitter", tags=["fitter-create"])
templates = Jinja2Templates(directory="app/server/templates")


@fitter_create_router.get(
    "", name="fitter-create:create-fitter-page", response_model=None
)
async def create_fitter_page(
    *,
    request: Request,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    lead_fitter: FitterRead = Depends(lead_fitter),
):
    stores = store_repo.get_all_stores()
    return templates.TemplateResponse(
        "create-fitter.html",
        {
            "title": "Fittr - Create Fitter",
            "request": request,
            "active_fitter": lead_fitter,
            "states": list(map(lambda state: state.value, State._member_map_.values())),
            "roles": list(map(lambda role: role.value, Role._member_map_.values())),
            "stores": stores,
        },
    )


@fitter_create_router.post(
    "", name="fitter-create:create-fitter-page-form", response_model=None
)
async def create_fitter_page_form(
    *,
    store_id: int = Form(...),
    request: Request,
    fitter_create: FitterCreate = Depends(FitterCreate.as_form),
    address_create: AddressCreate = Depends(AddressCreate.as_form),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
    lead_fitter: FitterRead = Depends(lead_fitter),
):
    db_address = address_repo.create_address(address_create=address_create)
    fitter_create.address_id = db_address.id
    fitter_create.store_id = store_id
    fitter_create.password = auth_service.hash_password(password=fitter_create.password)
    try:
        fitter_repo.create_fitter(fitter_create=fitter_create)
    except IntegrityError:
        address_repo.delete_address(address_id=db_address.id)
        stores = store_repo.get_all_stores()
        return templates.TemplateResponse(
            "create-fitter.html",
            {
                "title": "Fittr - Create Fitter",
                "request": request,
                "active_fitter": lead_fitter,
                "states": list(
                    map(lambda state: state.value, State._member_map_.values())
                ),
                "roles": list(map(lambda role: role.value, Role._member_map_.values())),
                "stores": stores,
                "errors": [f"Username '{fitter_create.username}' already exists"],
            },
        )
    return RedirectResponse("/fitters", status_code=303)
