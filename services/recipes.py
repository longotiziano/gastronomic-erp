from database.repositories.recipes import RecipeRepository
from services.base_service import BaseCrudService
from validators.bulk_base import BulkValidator

class RecipeService(BaseCrudService):
    repo: RecipeRepository

    def __init__(self):
        super().__init__(RecipeRepository())
        self.validator = BulkValidator(model=self.repo.model, repo=self.repo)  # type: ignore


    def bulk_create(self, recipes_data: list[dict]):
        """Creates multiple recipes in bulk. If one record fails, none are created. 
        Raises ValidationError if any record is invalid and """
        if not recipes_data:
            return []

        self.validator.bulk_validate(recipes_data)
        self.repo.bulk_create(recipes_data)
        return recipes_data


    def bulk_update(self, product_id: int, recipes_data: list[dict]):
        """Removes previous recipes and creates new ones in bulk. 
        If one record fails, none are created and previous recipes are not deleted. 
        Raises ValidationError if any record is invalid."""
        if not recipes_data:
            return []

        self.validator.bulk_validate([
            {"product_id": product_id, 
             "raw_material_id": r["raw_material_id"], 
             "amount": r["amount"]
            }
            for r in recipes_data
        ])
        self.repo.sync_product_recipes(product_id, recipes_data)
        return recipes_data