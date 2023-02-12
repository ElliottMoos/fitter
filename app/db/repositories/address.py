from typing import List
from sqlmodel import select, Session

from .base import BaseRepository
from app.models import (
    AddressCreate,
    AddressRead,
    AddressUpdate,
    Address,
    AddressReadAllRelations,
)


class AddressRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_all_addresses(self) -> List[AddressRead]:
        return self.session.exec(select(Address)).all()

    def create_address(self, address_create: AddressCreate) -> AddressRead:
        db_address = Address.from_orm(address_create)
        self.session.add(db_address)
        self.session.commit()
        self.session.refresh(db_address)
        return db_address

    def get_address_by_id(self, address_id: int) -> AddressReadAllRelations:
        return self.session.get(Address, address_id)

    def update_address(
        self, address_update: AddressUpdate, address_id: int
    ) -> AddressRead:
        db_address = self.session.get(Address, address_id)
        if not db_address:
            return
        address_data = address_update.dict(exclude_unset=True)
        for key, value in address_data.items():
            setattr(db_address, key, value)
        self.session.add(db_address)
        self.session.commit()
        self.session.refresh(db_address)
        return db_address

    def delete_address(self, address_id: int) -> AddressRead:
        db_address = self.session.get(Address, address_id)
        if not db_address:
            return
        self.session.delete(db_address)
        self.session.commit()
        return db_address
