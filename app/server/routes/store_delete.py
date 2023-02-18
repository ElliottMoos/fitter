from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import lead_fitter
from app.db.repositories.store import StoreRepository


store_delete_router = APIRouter(prefix="/delete-store", tags=["store-delete"])
templates = Jinja2Templates(directory="app/server/templates")


@store_delete_router.get(
    "/{store_id}", name="store-delete:delete-store", dependencies=[Depends(lead_fitter)]
)
async def delete_store(
    *,
    store_id: int,
    store_repo: StoreRepository = Depends(get_repository(StoreRepository)),
):
    store = store_repo.get_store_by_id(store_id=store_id)
    if store:
        store_repo.delete_store(store_id=store_id)
        return RedirectResponse("/stores")
    raise HTTPException(status_code=404, detail="Store not found")
