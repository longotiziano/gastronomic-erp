from typing import Optional
from database import db
from database.repositories.base import BaseRepository
from database.models.employee import Employee, EmployeeRole


class EmployeeRepository(BaseRepository[Employee]):
    model = Employee

    def get_by_bar(self, bar_id: int, active_only: bool = True) -> list[Employee]:
        query = db.session.query(Employee).filter_by(bar_id=bar_id)
        if active_only:
            query = query.filter(Employee.leave_at == None)  # noqa: E711
        return query.all()

    def get_by_role(self, rol: EmployeeRole, bar_id: Optional[int] = None) -> list[Employee]:
        query = db.session.query(Employee).filter_by(rol=rol)
        if bar_id is not None:
            query = query.filter_by(bar_id=bar_id)
        return query.all()

    def get_by_user(self, user_id: int) -> Optional[Employee]:
        return db.session.query(Employee).filter_by(user_id=user_id).first()

    def fire(self, id: int) -> Optional[Employee]:
        """Set leave_at to now, marking the employee as no longer active."""
        from datetime import datetime, timezone
        return self.update(id, leave_at=datetime.now(timezone.utc))