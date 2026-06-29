from typing import Optional
from database import db
from database.repositories.base import BaseRepository
from database.models.user import User


class UserRepository(BaseRepository[User]):
    model = User

    def get_by_email(self, email: str) -> Optional[User]:
        return db.session.query(User).filter_by(email=email).first()

    def get_active_by_email(self, email: str) -> Optional[User]:
        return (
            db.session.query(User)
            .filter_by(email=email, record_status=True)
            .first()
        )