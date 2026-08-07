from collections import defaultdict

from database.repositories.products import ProductCategoryRepository, ProductRepository
from services.recipes import RecipeService
from validators.bulk_base import BulkValidator
from database.models.product import ProductCategory
from services.base_service import BaseCrudService
from database.models.recipe import Recipe

class ProductService(BaseCrudService):
    repo: ProductRepository
    
    def __init__(self):
        super().__init__(ProductRepository())
        
        
    def get_most_used_category(self) -> ProductCategory | None:
        return self.repo._get_most_used_category()
        

    def _get_table_rows(self, items) -> list[dict]:
        """Obtains the table's rows, including the recipes for each product."""
        rows = super()._get_table_rows(items)
        recipes_by_product = self._get_products_recipes([r["data"] for r in rows])

        for r in rows:
            prod_id = r["data"].get("id")
            if prod_id:
                r["data"]["recipes"] = recipes_by_product.get(prod_id, [])

        return rows
        

    def _get_products_recipes(self, products: list[dict]) -> dict[int, list[dict]]:
        """Obtains the recipes for a list of dicts of products."""
        prods = [p.get("id") for p in products if p.get("id")]
        recipes: list[Recipe] = self.repo.get_by_values("product_id", prods, model=Recipe)

        recipes_by_product = defaultdict(list)
        for rec in recipes:
            recipes_by_product[rec.product_id].append({
                "raw_material_id": rec.raw_material_id,
                "name": rec.raw_material.name,
                "amount": rec.amount,
                "uom": rec.raw_material.uom.value,
            })
        return recipes_by_product


    def create(self, **kwargs):
        """Creates a product and its associated recipes. First the product, then the recipes.
        In case of error in any recipe, the product is created but the recipes are not."""
        recipes_data = kwargs.pop("recipes", [])
        product = super().create(**kwargs)

        if recipes_data:
            RecipeService().bulk_create([
                {"product_id": product.id, "raw_material_id": rec["raw_material_id"], "amount": rec["amount"]}
                for rec in recipes_data
            ])
        else:
            print(f"No recipes provided for product {product}.")

        return product


    def update(self, id: int, data: dict):
        """Updates a product and its associated recipes. First the product, then the recipes.
        In case of error in any recipe, the product is updated but the recipes are not."""
        recipes_data = data.pop("recipes", [])
        product_data = data.pop("product_data", {})

        if product_data:
            super().update(id, product_data)

        if recipes_data:
            for r in recipes_data:
                print(r)
            RecipeService().bulk_update(id, recipes_data)

    
class ProductCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductCategoryRepository())