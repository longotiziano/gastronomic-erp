from database.models.product import Product, ProductCategory, ProductSector
from database.repositories.products import ProductCategoryRepository, ProductRepository
from services.base import BaseService


class ProductCategoryService(BaseService):
    def __init__(self):
        super().__init__(ProductCategoryRepository(), check_existence="name")

    def get_by_sector(self, sector: ProductSector):
        return self.repository.get_by_sector(sector)


class ProductService(BaseService):
    def __init__(self):
        super().__init__(ProductRepository(), check_existence="name")

    def get_by_bar(self, bar_id: int, active_only: bool = True):
        return self.repository.get_by_bar(bar_id, active_only=active_only)

    def get_by_category(self, category_id: int, active_only: bool = True):
        return self.repository.get_by_category(category_id, active_only=active_only)
