from database import db
from database.repositories.base import BaseRepository
from database.models.product import Product, ProductCategory
from sqlalchemy import func

class ProductCategoryRepository(BaseRepository[ProductCategory]):
    model = ProductCategory


class ProductRepository(BaseRepository[Product]):
    model = Product
    
    def _get_most_used_category(self) -> ProductCategory | None:
        """Returns the most used category in database"""
        result = (
            db.session.query(ProductCategory, func.count(Product.id).label("total"))
            .join(Product, Product.category_id == ProductCategory.id)
            .group_by(ProductCategory.id)
            .order_by(func.count(Product.id).desc())
            .first()
        )
        return result[0] if result else None