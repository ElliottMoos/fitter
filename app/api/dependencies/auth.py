from fastapi import Depends, Cookie

from app.models.fitter import FitterRead
from app.db.repositories.fitter import FitterRepository
from app.api.dependencies.database import get_repository
from app.services import auth_service


def get_fitter_from_session_token(
    session_token: str = Cookie(default=None),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
) -> FitterRead | None:
    username = auth_service.get_fitter_username_from_token(session_token)
    return fitter_repo.get_fitter_by_username(username)
