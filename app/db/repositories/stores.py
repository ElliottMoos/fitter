from typing import List
from sqlmodel import select, Session

from .base import BaseRepository
from app.models.store import StoreCreate, StoreRead, StoreUpdate, Store


class StoreRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_stores(self) -> List[StoreRead]:
        return self.session.exec(select(Store)).all()

    def create_store(self, *, store_create: StoreCreate) -> StoreRead:
        db_store = Store.from_orm(store_create)
        self.session.add(db_store)
        self.session.commit()
        self.session.refresh(db_store)
        return db_store

    def get_store_by_id(self, *, store_id: int) -> StoreRead:
        return self.session.get(Store, store_id)

    def update_store(self, *, store_update: StoreUpdate, store_id: int) -> StoreRead:
        db_store = self.session.get(Store, store_id)
        if not db_store:
            return
        store_data = store_update.dict(exclude_unset=True)
        for key, value in store_data.items():
            setattr(db_store, key, value)
        self.session.add(db_store)
        self.session.commit()
        self.session.refresh(db_store)
        return db_store

    def delete_store(self, *, store_id: int) -> bool:
        db_store = self.session.get(Store, store_id)
        if not db_store:
            return False
        self.session.delete(db_store)
        self.session.commit()
        return True
