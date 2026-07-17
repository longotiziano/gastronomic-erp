from database.models.raw_material import RawMaterial
from database.repositories.raw_materials import RawMaterialCategoryRepository, RawMaterialRepository
from utils.exceptions import ConflictError, NotFoundError, ValidationError
from utils.helpers import clean_string


def obtain_raw_materials() -> list[RawMaterial]:
    repo = RawMaterialRepository()
    return repo.get_all(active_only=False)


def create_raw_material(name: str, category_id: int) -> RawMaterial:
    repo = RawMaterialRepository()
    name = clean_string(name, title=True)
    if not name:
        raise ValidationError("El nombre de la materia prima es requerido.")

    category_repo = RawMaterialCategoryRepository()
    category = category_repo.get_by_id(category_id)
    if category is None:
        raise NotFoundError("Categoría no encontrada.")

    raw_material = repo.create(name=name, category_id=category_id)
    if not raw_material:
        raise ConflictError("No se pudo crear la materia prima.")

    return raw_material


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
        category_repo = RawMaterialCategoryRepository()
        category = category_repo.get_by_id(updates["category_id"])
        if category is None:
            raise NotFoundError("Categoría no encontrada.")
        processed_updates["category_id"] = updates["category_id"]

    if not processed_updates:
        raise ValidationError("No hay campos válidos para actualizar")

    repo = RawMaterialRepository()
    raw_material = repo.update(raw_material_id, **processed_updates)
    if raw_material is None:
        raise ConflictError(f"No se ha podido actualizar la materia prima con ID {raw_material_id}.")


def alt_raw_material_status(raw_material_id: int) -> RawMaterial:
    repo = RawMaterialRepository()
    raw_material = repo.get_by_id(raw_material_id)
    if not raw_material:
        raise NotFoundError("Materia prima no encontrada.")

    raw_material.record_status = not raw_material.record_status
    updated_raw_material = repo.update(raw_material_id, record_status=raw_material.record_status)
    if not updated_raw_material:
        raise ConflictError("No se pudo actualizar el estado de la materia prima.")

    return updated_raw_material
