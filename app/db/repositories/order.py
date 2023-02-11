from typing import List
from sqlmodel import select, Session

from .base import BaseRepository
from app.models.order_product import OrderCreate, OrderRead, OrderUpdate, Order


class OrderRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_orders(self) -> List[OrderRead]:
        return self.session.exec(select(Order)).all()

    def create_order(self, order_create: OrderCreate) -> OrderRead:
        db_order = Order.from_orm(order_create)
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        return db_order

    def get_order_by_id(self, order_id: int) -> OrderRead:
        return self.session.get(Order, order_id)

    def update_order(self, order_update: OrderUpdate, order_id: int) -> OrderRead:
        db_order = self.session.get(Order, order_id)
        if not db_order:
            return
        order_data = order_update.dict(exclude_unset=True)
        for key, value in order_data.items():
            setattr(db_order, key, value)
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        return db_order

    def delete_order(self, order_id: int) -> bool:
        db_order = self.session.get(Order, order_id)
        if not db_order:
            return False
        self.session.delete(db_order)
        self.session.commit()
        return True
