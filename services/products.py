from collections import defaultdict

from database.repositories.products import ProductCategoryRepository, ProductRepository
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
        print(f"Recipes by product: {recipes_by_product}")
        return recipes_by_product


    
class ProductCategoryService(BaseCrudService):
    def __init__(self):
        super().__init__(ProductCategoryRepository())