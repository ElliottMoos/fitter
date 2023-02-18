from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import lead_fitter
from app.db.repositories.fitter import FitterRepository
from app.models.models import FitterRead


fitter_delete_router = APIRouter(prefix="/delete-fitter", tags=["fitter-delete"])
templates = Jinja2Templates(directory="app/server/templates")


@fitter_delete_router.get(
    "/{fitter_id}",
    name="fitter-delete:delete-fitter",
)
async def delete_fitter(
    *,
    fitter_id: int,
    lead_fitter: FitterRead = Depends(lead_fitter),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
):
    fitter = fitter_repo.get_fitter_by_id(fitter_id=fitter_id)
    if fitter:
        if fitter != lead_fitter:
            fitter_repo.delete_fitter(fitter_id=fitter_id)
            return RedirectResponse("/fitters")
        raise HTTPException(
            status_code=400, detail="Active fitter cannot delete itself"
        )
    raise HTTPException(status_code=404, detail="Fitter not found")
