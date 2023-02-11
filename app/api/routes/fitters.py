from typing import List
from fastapi import Depends, APIRouter

from app.services import auth_service
from app.api.dependencies.database import get_repository
from app.models.fitter import FitterCreate, FitterRead, FitterUpdate
from app.db.repositories.fitter import FitterRepository


fitters_router = APIRouter(prefix="/fitters", tags=["fitters"])


@fitters_router.get(
    "",
    response_model=List[FitterRead],
    name="fitters:get-fitters",
)
async def get_fitters(
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> List[FitterRead]:
    return fitter_repo.get_all_fitters()


@fitters_router.post(
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


@fitters_router.get(
    "/{fitter_id}",
    response_model=FitterRead,
    name="fitters:get-fitter",
)
async def get_fitter(
    *,
    fitter_id: int,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterRead:
    return fitter_repo.get_fitter_by_id(fitter_id=fitter_id)


@fitters_router.put(
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
