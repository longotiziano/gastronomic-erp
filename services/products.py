from services.base_service import BaseCrudService
from database.repositories.products import ProductCategoryRepository, ProductCategoryRepository, ProductRepository

class ProductService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductRepository(), entity_name="producto")
        
class ProductCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductCategoryRepository(), entity_name="categoría de producto")