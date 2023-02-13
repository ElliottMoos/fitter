from typing import List
from fastapi import Depends, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.server.dependencies.auth import get_fitter_from_session_token
from app.server.dependencies.pagination import get_paginator, Paginator
from app.server.dependencies.database import get_repository
from app.models import (
    StoreCreate,
    StoreRead,
    StoreUpdate,
    StoreReadAllRelations,
    FitterRead,
)
from app.db.repositories.store import StoreRepository


stores_api_router = APIRouter(prefix="/stores", tags=["stores"])
stores_template_router = APIRouter(prefix="/stores", tags=["stores"])
templates = Jinja2Templates(directory="app/server/templates")


@stores_api_router.get(
    "",
    response_model=List[StoreRead],
    name="stores:get-stores",
)
async def get_stores(
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
) -> List[StoreRead]:
    return store_repo.get_all_stores()


@stores_api_router.post(
    "",
    response_model=StoreRead,
    name="stores:create-store",
)
async def create_store(
    *,
    store_create: StoreCreate,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
) -> StoreRead:
    return store_repo.create_store(store_create=store_create)


@stores_api_router.get(
    "/{store_id}",
    response_model=StoreReadAllRelations,
    name="stores:get-store",
)
async def get_store(
    *,
    store_id: int,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
) -> StoreReadAllRelations:
    return store_repo.get_store_by_id(store_id=store_id)


@stores_api_router.put(
    "/{store_id}",
    response_model=StoreRead,
    name="stores:update-store",
)
async def update_store(
    *,
    store_id: int,
    store_update: StoreUpdate,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
) -> StoreRead:
    return store_repo.update_store(store_update=store_update, store_id=store_id)


@stores_api_router.delete(
    "/{store_id}",
    response_model=StoreRead,
    name="stores:delete-store",
)
async def delete_store(
    *,
    store_id: int,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
) -> StoreRead:
    return store_repo.delete_store(store_id=store_id)


@stores_template_router.get("", name="stores:stores-page")
async def stores_page(
    *,
    request: Request,
    paginator: Paginator[StoreRead] = Depends(get_paginator(StoreRead)),
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        page = paginator.paginate(store_repo.get_all_stores())
        return templates.TemplateResponse(
            "stores.html",
            {
                "title": "Fittr - Stores",
                "request": request,
                "page": page,
                "active_fitter": active_fitter,
            },
        )
    return RedirectResponse("/login")


@stores_template_router.get("/{store_id}", name="stores:store-page")
async def store_page(
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
                "store.html",
                {
                    "title": "Fittr - Stores",
                    "request": request,
                    "store": store,
                    "active_fitter": active_fitter,
                },
            )
    return RedirectResponse("/login")
