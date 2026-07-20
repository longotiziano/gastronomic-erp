from database.models.bar import Bar
from database.repositories.bars import BarRepository
from seeds.bars import validate_bar_name
from services.base_service import BaseCrudService
from utils.helpers import clean_string

_service = BaseCrudService(BarRepository(), entity_name="bar")


def obtain_bars() -> list[Bar]:
    return _service.repo.get_all(active_only=False)


def create_bar(name: str, address: str) -> Bar:
    name = clean_string(name, title=True)
    address = clean_string(address)

    validate_bar_name(name)

    return _service.create(field_existence={"name": name}, name=name, address=address)


def update_bar(bar_id: int, updates: dict) -> None:
    processed_updates = {}
    field_existence = {}

    if updates.get("name"):
        name = clean_string(updates["name"], title=True)
        validate_bar_name(name)
        processed_updates["name"] = name
        field_existence["name"] = name

    if updates.get("address"):
        processed_updates["address"] = clean_string(updates["address"])

    _service.update(bar_id, processed_updates, field_existence)


def alt_bar_status(bar_id: int) -> Bar:
    return _service.alt_status(bar_id)