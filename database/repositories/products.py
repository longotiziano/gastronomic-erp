from database import db
from database.repositories.base import BaseRepository
from database.models.product import Product, ProductCategory, ProductSector


class ProductCategoryRepository(BaseRepository[ProductCategory]):
    model = ProductCategory

    def get_by_sector(self, sector: ProductSector) -> list[ProductCategory]:
        return db.session.query(ProductCategory).filter_by(sector=sector).all()


class ProductRepository(BaseRepository[Product]):
    model = Product

    def get_by_bar(self, bar_id: int, active_only: bool = True) -> list[Product]:
        query = db.session.query(Product).filter_by(bar_id=bar_id)
        if active_only:
            query = query.filter(Product.record_status == True)  # noqa: E712
        return query.all()

    def get_by_category(self, category_id: int, active_only: bool = True) -> list[Product]:
        query = db.session.query(Product).filter_by(category_id=category_id)
        if active_only:
            query = query.filter(Product.record_status == True)  # noqa: E712
        return query.all()