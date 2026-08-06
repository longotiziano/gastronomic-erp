from database.repositories.recipes import RecipeRepository
from services.base_service import BaseCrudService

class RecipeService(BaseCrudService):
    repo: RecipeRepository

    def __init__(self):
        super().__init__(RecipeRepository())