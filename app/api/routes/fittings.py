from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import Depends, APIRouter, Query

from app.api.dependencies.database import get_repository
from app.models.fitting import FittingCreate, FittingRead, FittingUpdate
from app.db.repositories.fitting import FittingRepository


fittings_router = APIRouter(prefix="/fittings", tags=["fittings"])


class FittingsStartEndFilter(BaseModel):
    start: Optional[datetime] = Query(default=None)
    end: Optional[datetime] = Query(default=None)


@fittings_router.get(
    "",
    response_model=List[FittingRead],
    name="fittings:get-fittings",
)
async def get_fittings(
    start_end_filter: FittingsStartEndFilter = Depends(),
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> List[FittingRead]:
    if start_end_filter.start and start_end_filter.end:
        return fitting_repo.get_fittings_start_end(
            start_end_filter.start, start_end_filter.end
        )
    elif start_end_filter.start and not start_end_filter.end:
        return fitting_repo.get_fittings_start(start_end_filter.start)
    elif start_end_filter.end and not start_end_filter.start:
        return fitting_repo.get_fittings_end(start_end_filter.end)
    return fitting_repo.get_all_fittings()


@fittings_router.post(
    "",
    response_model=FittingRead,
    name="fittings:create-fitting",
)
async def create_fitting(
    *,
    fitting_create: FittingCreate,
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> FittingRead:
    return fitting_repo.create_fitting(fitting_create=fitting_create)


@fittings_router.get(
    "/{fitting_id}",
    response_model=FittingRead,
    name="fittings:get-fitting",
)
async def get_fitting(
    *,
    fitting_id: int,
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> FittingRead:
    return fitting_repo.get_fitting_by_id(fitting_id=fitting_id)


@fittings_router.put(
    "/{fitting_id}",
    response_model=FittingRead,
    name="fittings:update-fitting",
)
async def update_fitting(
    *,
    fitting_id: int,
    fitting_update: FittingUpdate,
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> FittingRead:
    return fitting_repo.update_fitting(
        fitting_update=fitting_update, fitting_id=fitting_id
    )


@fittings_router.delete(
    "/{fitting_id}",
    response_model=FittingRead,
    name="fittings:delete-fitting",
)
async def delete_fitting(
    *,
    fitting_id,
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> FittingRead:
    return fitting_repo.delete_fitting(fitting_id=fitting_id)
