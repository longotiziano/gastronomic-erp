from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.expense import Expense


class ExpenseRepository(BaseRepository[Expense]):
    model = Expense