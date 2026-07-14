from database.repositories.arqueo import ArqueoRepository
from services.base import BaseService


class ArqueoService(BaseService):
    def __init__(self):
        super().__init__(ArqueoRepository())

    def get_by_bar(self, bar_id: int):
        return self.repository.get_by_bar(bar_id)

    def get_by_date_range(self, bar_id: int, date_from, date_to):
        return self.repository.get_by_date_range(bar_id, date_from, date_to)

    def get_by_cashier(self, cashier_id: int):
        return self.repository.get_by_cashier(cashier_id)
