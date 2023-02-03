from typing import List
from sqlmodel import select, Session

from .base import BaseRepository
from app.models.fitting import FittingCreate, FittingRead, FittingUpdate, Fitting


class FittingRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_fittings(self) -> List[FittingRead]:
        return self.session.exec(select(Fitting)).all()

    def create_fitting(self, *, fitting_create: FittingCreate) -> FittingRead:
        db_fitting = Fitting.from_orm(fitting_create)
        self.session.add(db_fitting)
        self.session.commit()
        self.session.refresh(db_fitting)
        return db_fitting

    def get_fitting_by_id(self, *, fitting_id: int) -> FittingRead:
        return self.session.get(Fitting, fitting_id)

    def update_fitting(
        self, *, fitting_update: FittingUpdate, fitting_id: int
    ) -> FittingRead:
        db_fitting = self.session.get(Fitting, fitting_id)
        if not db_fitting:
            return
        fitting_data = fitting_update.dict(exclude_unset=True)
        for key, value in fitting_data.items():
            setattr(db_fitting, key, value)
        self.session.add(db_fitting)
        self.session.commit()
        self.session.refresh(db_fitting)
        return db_fitting

    def delete_fitting(self, *, fitting_id: int) -> bool:
        db_fitting = self.session.get(Fitting, fitting_id)
        if not db_fitting:
            return False
        self.session.delete(db_fitting)
        self.session.commit()
        return True
