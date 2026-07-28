from database.repositories.products import ProductCategoryRepository, ProductRepository
from database.models.product import ProductCategory
from services.base_service import BaseCrudService

class ProductService(BaseCrudService):
    repo: ProductRepository
    
    def __init__(self):
        super().__init__(ProductRepository())
        
        
    def get_most_used_category(self) -> ProductCategory | None:
        return self.repo._get_most_used_category()
        
    
    
class ProductCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductCategoryRepository())