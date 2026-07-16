from typing import Optional

from database import db
from database.models.user import User, UserRole
from database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    def user_id_exists(self, user_id: int) -> bool:
        return db.session.query(User).filter_by(id=user_id).exists() is not None

    def get_by_email(self, email: str) -> Optional[User]:
        return db.session.query(User).filter_by(email=email).first()

    def get_active_by_email(self, email: str) -> Optional[User]:
        return db.session.query(User).filter_by(email=email, record_status=True).first()

    def get_by_bar(self, bar_id: int, active_only: bool = True) -> list[User]:
        query = db.session.query(User).filter_by(bar_id=bar_id)
        if active_only:
            query = query.filter(User.leave_at == None)  # noqa: E711
        return query.all()

    def get_by_role(self, rol: UserRole, bar_id: Optional[int] = None) -> list[User]:
        query = db.session.query(User).filter_by(rol=rol)
        if bar_id is not None:
            query = query.filter_by(bar_id=bar_id)
        return query.all()

    def get_by_user(self, user_id: int) -> Optional[User]:
        return db.session.query(User).filter_by(id=user_id).first()

    def fire(self, id: int) -> Optional[User]:
        """Set leave_at to now, marking the employee as no longer active."""
        from datetime import datetime, timezone

        return self.update(id, leave_at=datetime.now(timezone.utc))