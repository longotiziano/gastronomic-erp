from services.base_service import BaseCrudService
from database.repositories.bars import BarRepository

class BarService(BaseCrudService):
    def __init__(self):
        super().__init__(BarRepository())