from database.repositories.recipes import RecipeRepository
from services.base import BaseService


class RecipeService(BaseService):
    def __init__(self):
        super().__init__(RecipeRepository())

    def get_by_product(self, product_id: int):
        return self.repository.get_by_product(product_id)

    def get_by_raw_material(self, raw_material_id: int):
        return self.repository.get_by_raw_material(raw_material_id)

    def get_ingredient(self, product_id: int, raw_material_id: int):
        return self.repository.get_ingredient(product_id, raw_material_id)
