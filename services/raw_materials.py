from services.base_service import BaseCrudService
from database.repositories.raw_materials import RawMaterialRepository, RawMaterialCategoryRepository

class RawMaterialService(BaseCrudService):
    def __init__(self):
        super().__init__(RawMaterialRepository(), entity_name="materia prima")

class RawMaterialCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(RawMaterialCategoryRepository(), entity_name="categoría de materia prima")