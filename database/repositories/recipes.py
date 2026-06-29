from database import db
from database.repositories.base import BaseRepository
from database.models.recipe import Recipe


class RecipeRepository(BaseRepository[Recipe]):
    model = Recipe

    def get_by_product(self, product_id: int) -> list[Recipe]:
        """Return all ingredients (raw materials) for a given product."""
        return db.session.query(Recipe).filter_by(product_id=product_id).all()

    def get_by_raw_material(self, raw_material_id: int) -> list[Recipe]:
        """Return all recipes that use a given raw material."""
        return db.session.query(Recipe).filter_by(raw_material_id=raw_material_id).all()

    def get_ingredient(self, product_id: int, raw_material_id: int) -> Recipe | None:
        """Return the specific recipe row for a product + raw material pair."""
        return (
            db.session.query(Recipe)
            .filter_by(product_id=product_id, raw_material_id=raw_material_id)
            .first()
        )