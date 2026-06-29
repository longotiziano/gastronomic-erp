from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.expense import Expense


class ExpenseRepository(BaseRepository[Expense]):
    model = Expense

    def get_by_date_range(self, date_from: date, date_to: date) -> list[Expense]:
        return (
            db.session.query(Expense)
            .filter(
                Expense.created_at >= date_from,
                Expense.created_at <= date_to,
            )
            .all()
        )

    def get_by_payment_type(self, payment_type: str) -> list[Expense]:
        return db.session.query(Expense).filter_by(payment_type=payment_type).all()