from typing import List
from fastapi import Depends, APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from app.services import auth_service
from app.server.dependencies.auth import active_fitter
from app.server.dependencies.database import get_repository
from app.server.dependencies.pagination import Paginator, get_paginator
from app.models import FitterCreate, FitterRead, FitterUpdate, FitterReadAllRelations
from app.db.repositories.fitter import FitterRepository


fitters_api_router = APIRouter(prefix="/fitters", tags=["fitters"])
fitters_template_router = APIRouter(prefix="/fitters", tags=["fitters"])
templates = Jinja2Templates(directory="app/server/templates")


@fitters_api_router.get(
    "",
    response_model=List[FitterRead],
    name="fitters:get-fitters",
)
async def get_fitters(
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> List[FitterRead]:
    return fitter_repo.get_all_fitters()


@fitters_api_router.post(
    "",
    response_model=FitterRead,
    name="fitters:create-fitter",
)
async def create_fitter(
    *,
    fitter_create: FitterCreate,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterRead:
    fitter_create.password = auth_service.hash_password(password=fitter_create.password)
    return fitter_repo.create_fitter(fitter_create=fitter_create)


@fitters_api_router.get(
    "/{fitter_id}",
    response_model=FitterReadAllRelations,
    name="fitters:get-fitter",
)
async def get_fitter(
    *,
    fitter_id: int,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterReadAllRelations:
    return fitter_repo.get_fitter_by_id(fitter_id=fitter_id)


@fitters_api_router.put(
    "/{fitter_id}",
    response_model=FitterRead,
    name="fitters:update-fitter",
)
async def update_fitter(
    *,
    fitter_id: int,
    fitter_update: FitterUpdate,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterRead:
    return fitter_repo.update_fitter(fitter_update=fitter_update, fitter_id=fitter_id)


@fitters_api_router.delete(
    "/{fitter_id}",
    response_model=FitterRead,
    name="fitters:delete-fitter",
)
async def delete_fitter(
    *,
    fitter_id: int,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterRead:
    return fitter_repo.delete_fitter(fitter_id=fitter_id)


@fitters_template_router.get("", name="fitters:fitters-page")
async def fitters_page(
    *,
    request: Request,
    paginator: Paginator[FitterRead] = Depends(get_paginator(FitterRead)),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
    active_fitter: FitterRead = Depends(active_fitter),
):
    page = paginator.paginate(fitter_repo.get_all_fitters())
    return templates.TemplateResponse(
        "fitters.html",
        {
            "title": "Fittr - Fitters",
            "request": request,
            "page": page,
            "active_fitter": active_fitter,
        },
    )


@fitters_template_router.get("/{fitter_id}", name="fitters:fitter-page")
async def fitter_page(
    *,
    fitter_id: int,
    request: Request,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
    active_fitter: FitterRead = Depends(active_fitter),
):
    fitter = fitter_repo.get_fitter_by_id(fitter_id=fitter_id)
    if fitter:
        return templates.TemplateResponse(
            "fitter.html",
            {
                "title": "Fittr - Fitter",
                "request": request,
                "fitter": fitter,
                "active_fitter": active_fitter,
            },
        )
    raise HTTPException(status_code=404, detail="Fitter not found")
