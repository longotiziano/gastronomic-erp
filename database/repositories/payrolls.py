from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.payroll import Payroll


class PayrollRepository(BaseRepository[Payroll]):
    model = Payroll

    def get_by_employee(self, employee_id: int) -> list[Payroll]:
        return db.session.query(Payroll).filter_by(employee_id=employee_id).all()

    def get_by_date_range(self, employee_id: int, date_from: date, date_to: date) -> list[Payroll]:
        return (
            db.session.query(Payroll)
            .filter(
                Payroll.employee_id == employee_id,
                Payroll.day >= date_from,
                Payroll.day <= date_to,
            )
            .all()
        )

    def is_day_paid(self, employee_id: int, day: date) -> bool:
        """Check if a specific day has already been paid for an employee."""
        return (
            db.session.query(Payroll)
            .filter_by(employee_id=employee_id, day=day)
            .first()
        ) is not None