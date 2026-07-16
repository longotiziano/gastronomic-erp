from database.models.bar import Bar
from database.repositories.bars import BarRepository
from utils.exceptions import ConflictError
from utils.helpers import clean_string

def create_bar(name: str, address: str) -> Bar:
    bar_repo = BarRepository()
    name = clean_string(name, title=True)
    address = clean_string(address)
    if bar_repo.get_by_name(name):
        raise ConflictError("El bar ya se encuentra registrado.")

    bar = bar_repo.create(name=name, address=address)
    if not bar:
        raise ConflictError("No se pudo crear el bar.")

    return bar