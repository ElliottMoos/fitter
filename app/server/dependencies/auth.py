from fastapi import Depends, Cookie
from fastapi.exceptions import HTTPException

from app.models import FitterRead, Role
from app.db.repositories.fitter import FitterRepository
from app.server.dependencies.database import get_repository
from app.services import auth_service


class RequiresLoginException(Exception):
    pass


def get_fitter_from_session_token(
    session_token: str = Cookie(default=None),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterRead | None:
    username = auth_service.get_fitter_username_from_token(session_token)
    return fitter_repo.get_fitter_by_username(username)


def active_fitter(
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
) -> FitterRead:
    if active_fitter:
        return active_fitter
    raise RequiresLoginException


def lead_fitter(active_fitter: FitterRead = Depends(active_fitter)) -> FitterRead:
    if active_fitter.role == Role.Lead:
        return active_fitter
    raise HTTPException(status_code=403, detail="Unauthorized")
