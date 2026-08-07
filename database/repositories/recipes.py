from sqlalchemy.exc import IntegrityError

from database import db
from database.repositories.base import BaseRepository
from database.models.recipe import Recipe
from utils.exceptions import ConflictError


class RecipeRepository(BaseRepository[Recipe]):
    model = Recipe


    def sync_product_recipes(self, product_id: int, recipes: list[dict]) -> list[Recipe]:
        """
        Replaces ALL recipes of a product with a new set, in a single transaction.
        """
        self.bulk_delete(product_id=product_id, model=self.model)
        print(recipes)
        instances = [self.model(product_id=product_id, **r) for r in recipes] # type: ignore
        db.session.add_all(instances)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ConflictError("Uno o más ingredientes de la receta violan una restricción.") from e

        for instance in instances:
            db.session.refresh(instance)

        return instances