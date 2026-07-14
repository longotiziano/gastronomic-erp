from datetime import datetime, timezone

from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    employee = db.relationship("Employee", back_populates="user", uselist=False)

    def soft_delete(self) -> None:
        self.record_status = False

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} email={self.email!r} active={self.record_status}>"
