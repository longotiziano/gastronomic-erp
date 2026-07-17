from database.models.bar import Bar
from database.repositories.bars import BarRepository
from utils.exceptions import NotFoundError, ValidationError


def validate_bar_name(name: str):
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("El nombre del bar es requerido.")


def validate_bar_id(bar_id: int):
    bar_repo = BarRepository()
    if not isinstance(bar_id, int):
        raise ValidationError("El ID del bar debe ser un número entero.")

    if bar_id < 0:
        raise ValidationError("El ID del bar no puede ser negativo.")

    if not bar_repo.bar_id_exists(bar_id):
        raise NotFoundError(f"Bar con ID {bar_id} no existe.")