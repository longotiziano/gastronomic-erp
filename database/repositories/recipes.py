from database import db
from database.repositories.base import BaseRepository
from database.models.recipe import Recipe


class RecipeRepository(BaseRepository[Recipe]):
    model = Recipe