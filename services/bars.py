from database.models.bar import Bar
from database.repositories.bars import BarRepository
from seeds.bars import validate_bar_name
from utils.exceptions import ConflictError, NotFoundError, ValidationError
from utils.helpers import clean_string


def obtain_bars() -> list[Bar]:
    bar_repo = BarRepository()
    return bar_repo.get_all(active_only=False)


def create_bar(name: str, address: str) -> Bar:
    bar_repo = BarRepository()
    name = clean_string(name, title=True)
    address = clean_string(address)

    validate_bar_name(name)

    if bar_repo.get_by_name_case_insensitive(name):
        raise ConflictError("El bar ya se encuentra registrado.")

    bar = bar_repo.create(name=name, address=address)
    if not bar:
        raise ConflictError("No se pudo crear el bar.")

    return bar


def update_bar(bar_id: int, updates: dict) -> None:
    if not updates:
        raise ValidationError("No hay campos para actualizar")

    processed_updates = {}
    if updates.get("name"):
        name = clean_string(updates["name"], title=True)
        validate_bar_name(name)
        processed_updates["name"] = name

    if updates.get("address") is not None:
        processed_updates["address"] = clean_string(updates["address"])

    if not processed_updates:
        raise ValidationError("No hay campos válidos para actualizar")

    bar_repo = BarRepository()
    bar = bar_repo.update(bar_id, **processed_updates)
    if bar is None:
        raise ConflictError(f"No se ha podido actualizar el bar con ID {bar_id}.")


def alt_bar_status(bar_id: int) -> Bar:
    bar_repo = BarRepository()
    bar = bar_repo.get_by_id(bar_id)
    if not bar:
        raise NotFoundError("Bar no encontrado.")

    bar.record_status = not bar.record_status
    updated_bar = bar_repo.update(bar_id, record_status=bar.record_status)
    if not updated_bar:
        raise ConflictError("No se pudo actualizar el estado del bar.")

    return updated_bar