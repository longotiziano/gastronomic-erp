from services.base_service import BaseCrudService
from database.repositories.raw_materials import RawMaterialRepository, RawMaterialCategoryRepository
from database.models.raw_material import Uom

class RawMaterialService(BaseCrudService):
    def __init__(self):
        super().__init__(RawMaterialRepository())
        
    def create(self, **data):
        uom = data.get("uom")
        if uom and isinstance(uom, Uom):
            data["uom"] = uom.value
        return super().create(**data)

class RawMaterialCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(RawMaterialCategoryRepository())