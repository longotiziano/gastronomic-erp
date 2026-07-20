from database.models.raw_material import RawMaterialCategory
from database.repositories.raw_materials import RawMaterialCategoryRepository
from services.base_service import BaseCrudService
from utils.exceptions import ValidationError
from utils.helpers import clean_string
from flask_sqlalchemy.pagination import Pagination

_service = BaseCrudService(RawMaterialCategoryRepository(), entity_name="categoría")


def obtain_raw_material_categories() -> Pagination:
    return _service.filter_sort("raw-materials-categories")


def create_raw_material_category(name: str) -> RawMaterialCategory:
    name = clean_string(name, title=True)
    if not name:
        raise ValidationError("El nombre de la categoría es requerido.")

    return _service.create(field_existence={"name": name}, name=name)


def update_raw_material_category(category_id: int, updates: dict) -> None:
    if not updates:
        raise ValidationError("No hay campos para actualizar")

    processed_updates = {}
    field_existence = {}

    if updates.get("name"):
        name = clean_string(updates["name"], title=True)
        if not name:
            raise ValidationError("El nombre de la categoría es requerido.")
        processed_updates["name"] = name
        field_existence["name"] = name

    _service.update(category_id, processed_updates, field_existence)


def alt_raw_material_category_status(category_id: int) -> RawMaterialCategory:
    return _service.alt_status(category_id)