from database.repositories.products import ProductCategoryRepository, ProductRepository
from services.base_service import BaseCrudService

class ProductService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductRepository())
        
class ProductCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductCategoryRepository())