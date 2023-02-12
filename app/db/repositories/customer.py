from typing import List
from sqlmodel import select, Session, col

from .base import BaseRepository
from app.models import (
    CustomerCreate,
    CustomerRead,
    CustomerUpdate,
    Customer,
    CustomerReadAllRelations,
)


class CustomerRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_customers(self) -> List[CustomerRead]:
        return self.session.exec(select(Customer)).all()

    def get_customers_name_search(
        self, first_name: str = "", last_name: str = ""
    ) -> List[CustomerRead]:
        return self.session.exec(
            select(Customer)
            .where(col(Customer.first_name).contains(first_name))
            .where(col(Customer.last_name).contains(last_name))
        ).all()

    def create_customer(self, customer_create: CustomerCreate) -> CustomerRead:
        db_customer = Customer.from_orm(customer_create)
        self.session.add(db_customer)
        self.session.commit()
        self.session.refresh(db_customer)
        return db_customer

    def get_customer_by_id(self, customer_id: int) -> CustomerReadAllRelations:
        return self.session.get(Customer, customer_id)

    def update_customer(
        self, customer_update: CustomerUpdate, customer_id: int
    ) -> CustomerRead:
        db_customer = self.session.get(Customer, customer_id)
        if not db_customer:
            return
        customer_data = customer_update.dict(exclude_unset=True)
        for key, value in customer_data.items():
            setattr(db_customer, key, value)
        self.session.add(db_customer)
        self.session.commit()
        self.session.refresh(db_customer)
        return db_customer

    def delete_customer(self, customer_id: int) -> CustomerRead:
        db_customer = self.session.get(Customer, customer_id)
        if not db_customer:
            return
        self.session.delete(db_customer)
        self.session.commit()
        return db_customer
