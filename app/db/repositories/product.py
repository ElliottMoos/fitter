from typing import List
from sqlmodel import select, Session

from .base import BaseRepository
from app.models.order_product import ProductCreate, ProductRead, ProductUpdate, Product


class ProductRepository(BaseRepository):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_all_products(self) -> List[ProductRead]:
        return self.session.exec(select(Product)).all()

    def create_product(self, product_create: ProductCreate) -> ProductRead:
        db_product = Product.from_orm(product_create)
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product

    def get_product_by_id(self, product_id: int) -> ProductRead:
        return self.session.get(Product, product_id)

    def update_product(
        self, product_update: ProductUpdate, product_id: int
    ) -> ProductRead:
        db_product = self.session.get(Product, product_id)
        if not db_product:
            return
        product_data = product_update.dict(exclude_unset=True)
        for key, value in product_data.items():
            setattr(db_product, key, value)
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int) -> bool:
        db_product = self.session.get(Product, product_id)
        if not db_product:
            return False
        self.session.delete(db_product)
        self.session.commit()
        return True
