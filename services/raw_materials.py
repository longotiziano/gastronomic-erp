from database.models.raw_material import RawMaterial
from database.repositories.raw_materials import RawMaterialCategoryRepository, RawMaterialRepository
from services.base_service import BaseCrudService
from utils.exceptions import NotFoundError, ValidationError
from utils.helpers import clean_string

_service = BaseCrudService(RawMaterialRepository(), entity_name="materia prima")
_category_repo = RawMaterialCategoryRepository()


def obtain_raw_materials() -> list[RawMaterial]:
    return _service.repo.get_all(active_only=False)


def create_raw_material(name: str, category_id: int) -> RawMaterial:
    name = clean_string(name, title=True)
    if not name:
        raise ValidationError("El nombre de la materia prima es requerido.")

    category = _category_repo.get_by_id(category_id)
    if category is None:
        raise NotFoundError("Categoría no encontrada.")

    return _service.create(name=name, category_id=category_id)


def update_raw_material(raw_material_id: int, updates: dict) -> None:
    if not updates:
        raise ValidationError("No hay campos para actualizar")

    processed_updates = {}

    if updates.get("name"):
        name = clean_string(updates["name"], title=True)
        if not name:
            raise ValidationError("El nombre de la materia prima es requerido.")
        processed_updates["name"] = name

    if updates.get("category_id"):
        category = _category_repo.get_by_id(updates["category_id"])
        if category is None:
            raise NotFoundError("Categoría no encontrada.")
        processed_updates["category_id"] = updates["category_id"]

    _service.update(raw_material_id, processed_updates)


def alt_raw_material_status(raw_material_id: int) -> RawMaterial:
    return _service.alt_status(raw_material_id)