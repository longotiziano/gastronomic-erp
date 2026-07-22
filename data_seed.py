from database import db
from database.models.raw_material import Uom
from database.models.user import UserRole
from services.bars import BarService
from services.products import ProductCategoryService, ProductService
from services.raw_materials import RawMaterialCategoryService, RawMaterialService
from services.users import UserService


def _find_existing(service, name: str, bar_id: int | None = None):
    normalized_name = name.strip().lower()

    if hasattr(service.repo, "get_by_name_case_insensitive"):
        existing = service.repo.get_by_name_case_insensitive(name)
        if existing:
            return existing

    records = service.repo.get_all(active_only=False)
    for record in records:
        record_name = getattr(record, "name", "")
        if not record_name:
            continue
        if record_name.strip().lower() != normalized_name:
            continue
        if bar_id is None or getattr(record, "bar_id", None) == bar_id:
            return record

    return None


def _get_or_create_bar(name: str = "Bar principal", address: str = "Calle 123"):
    service = BarService()
    existing = _find_existing(service, name)
    if existing:
        return existing
    return service.create(name=name, address=address)


def _get_or_create_user(bar_id: int):
    service = UserService()
    existing = service.repo.get_by_email("admin@example.com")
    if existing:
        return existing
    return service.create(
        name="Admin",
        email="admin@example.com",
        password="adminpassword",
        rol=UserRole.administrator,
        bar_id=bar_id,
        address="Admin Address",
        daily_salary=0.0,
    )


def _get_or_create_raw_material_category(name: str = "Carnes"):
    service = RawMaterialCategoryService()
    existing = _find_existing(service, name)
    if existing:
        return existing
    return service.create(name=name)


def _get_or_create_raw_material(category_id: int, name: str = "Carne picada"):
    service = RawMaterialService()
    existing = _find_existing(service, name)
    if existing:
        return existing
    return service.create(name=name, category_id=category_id, uom=Uom.gr)


def _get_or_create_product_category(name: str = "Bebidas"):
    service = ProductCategoryService()
    existing = _find_existing(service, name)
    if existing:
        return existing
    return service.create(name=name, sector="bar")


def _get_or_create_product(category_id: int, bar_id: int, name: str = "Coca Cola", price: float = 2.5):
    service = ProductService()
    existing = _find_existing(service, name, bar_id=bar_id)
    if existing:
        return existing
    return service.create(name=name, category_id=category_id, price=price, bar_id=bar_id)


def _ensure_recipe(product_id: int, raw_material_id: int, amount: float = 0.25):
    from database.models.recipe import Recipe
    from database.repositories.recipes import RecipeRepository
    repo = RecipeRepository()

    existing = db.session.query(Recipe).filter_by(product_id=product_id, raw_material_id=raw_material_id).first()
    if existing:
        return existing

    recipe = repo.create(product_id=product_id, raw_material_id=raw_material_id, amount=amount)
    return recipe


def _ensure_stock(raw_material_id: int, bar_id: int, amount: float = 10.0):
    from database.models.stock import Stock
    from database.repositories.stock import StockRepository
    repo = StockRepository()

    existing = db.session.query(Stock).filter_by(raw_material_id=raw_material_id, bar_id=bar_id).first()
    if existing:
        return existing

    stock = repo.create(raw_material_id=raw_material_id, bar_id=bar_id, amount=amount)
    return stock


def load_initial_data():
    bar = _get_or_create_bar()
    _get_or_create_user(bar.id)

    category = _get_or_create_raw_material_category()
    raw_material = _get_or_create_raw_material(category.id)

    product_category = _get_or_create_product_category()
    product = _get_or_create_product(product_category.id, bar.id)

    _ensure_recipe(product.id, raw_material.id)
    _ensure_stock(raw_material.id, bar.id)

    return {
        "bar": bar,
        "user": _get_or_create_user(bar.id),
        "raw_material_category": category,
        "raw_material": raw_material,
        "product_category": product_category,
        "product": product,
    }


if __name__ == "__main__":
    load_initial_data()
