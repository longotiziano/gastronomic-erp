import enum
from datetime import datetime, timezone

from database import db


class UserRole(enum.Enum):
    waiter = "waiter"
    cashier = "cashier"
    administrator = "administrator"
    receptionist = "receptionist"
    chef = "chef"
    chef_assistant = "chef_assistant"
    dishes = "dishes"
    manager = "manager"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    rol = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.waiter)
    leave_at = db.Column(db.DateTime, nullable=True)
    daily_salary = db.Column(db.Float, nullable=False, default=0.0)
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)

    filterable_fields = ["name", "email", "rol", "bar_id", "record_status"]

    # Relationships
    bar = db.relationship("Bar", back_populates="employees")
    payrolls = db.relationship("Payroll", back_populates="employee", lazy="dynamic")
    arqueos_as_cashier = db.relationship(
        "Arqueo",
        foreign_keys="Arqueo.cashier_id",
        back_populates="cashier",
        lazy="dynamic",
    )
    arqueos_as_manager = db.relationship(
        "Arqueo",
        foreign_keys="Arqueo.manager_id",
        back_populates="manager",
        lazy="dynamic",
    )

    def is_active(self) -> bool:
        return self.leave_at is None

    def soft_delete(self) -> None:
        self.record_status = False

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} name={self.name!r} email={self.email!r} "
            f"role={self.rol.value if self.rol else None} active={self.is_active()}>"
        )
