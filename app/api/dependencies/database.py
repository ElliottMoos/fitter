from typing import Callable, Type
from fastapi import Depends, Request
from sqlmodel import Session

from app.db.repositories import BaseRepository


def get_session(request: Request):
    return Session(request.app.state._engine)


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(session: Session = Depends(get_session)) -> Type[BaseRepository]:
        return repo_type(session)

    return get_repo
