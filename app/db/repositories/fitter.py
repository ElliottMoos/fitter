from typing import List
from sqlmodel import select, Session

from .base import BaseRepository
from app.models import (
    FitterCreate,
    FitterRead,
    FitterUpdate,
    Fitter,
    FitterReadAllRelations,
)


class FitterRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_fitters(self) -> List[FitterRead]:
        return self.session.exec(select(Fitter)).all()

    def create_fitter(self, fitter_create: FitterCreate) -> FitterRead:
        db_fitter = Fitter.from_orm(fitter_create)
        self.session.add(db_fitter)
        self.session.commit()
        self.session.refresh(db_fitter)
        return db_fitter

    def get_fitter_by_id(self, fitter_id: int) -> FitterReadAllRelations:
        return self.session.get(Fitter, fitter_id)

    def get_fitter_by_username(self, username: str) -> FitterReadAllRelations:
        results = self.session.exec(select(Fitter).where(Fitter.username == username))
        return results.first()

    def update_fitter(self, fitter_update: FitterUpdate, fitter_id: int) -> FitterRead:
        db_fitter = self.session.get(Fitter, fitter_id)
        if not db_fitter:
            return
        fitter_data = fitter_update.dict(exclude_unset=True)
        for key, value in fitter_data.items():
            setattr(db_fitter, key, value)
        self.session.add(db_fitter)
        self.session.commit()
        self.session.refresh(db_fitter)
        return db_fitter

    def delete_fitter(self, fitter_id: int) -> FitterRead:
        db_fitter = self.session.get(Fitter, fitter_id)
        if not db_fitter:
            return
        self.session.delete(db_fitter)
        self.session.commit()
        return db_fitter
