from typing import List
from fastapi import Depends, APIRouter

from app.api.dependencies.database import get_repository
from app.models import StoreCreate, StoreRead, StoreUpdate, StoreReadAllRelations
from app.db.repositories.store import StoreRepository


stores_router = APIRouter(prefix="/stores", tags=["stores"])


@stores_router.get(
    "",
    response_model=List[StoreRead],
    name="stores:get-stores",
)
async def get_stores(
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
) -> List[StoreRead]:
    return store_repo.get_all_stores()


@stores_router.post(
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


@stores_router.get(
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


@stores_router.put(
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


@stores_router.delete(
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
