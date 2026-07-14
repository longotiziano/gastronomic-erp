from database.repositories.raw_materials import RawMaterialCategoryRepository, RawMaterialRepository
from services.base import BaseService


class RawMaterialCategoryService(BaseService):
    def __init__(self):
        super().__init__(RawMaterialCategoryRepository(), check_existence="name")


class RawMaterialService(BaseService):
    def __init__(self):
        super().__init__(RawMaterialRepository(), check_existence="name")

    def get_by_category(self, category_id: int, active_only: bool = True):
        return self.repository.get_by_category(category_id, active_only=active_only)
