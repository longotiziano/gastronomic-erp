from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.payroll import Payroll


class PayrollRepository(BaseRepository[Payroll]):
    model = Payroll