import enum
from datetime import datetime, timezone

from database import db


class EmployeeRole(enum.Enum):
    waiter = "waiter"
    cashier = "cashier"
    administrator = "administrator"
    receptionist = "receptionist"
    chef = "chef"
    chef_assistant = "chef_assistant"
    dishes = "dishes"
    manager = "manager"


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)
    rol = db.Column(db.Enum(EmployeeRole), nullable=False)
    leave_at = db.Column(db.DateTime, nullable=True)
    daily_salary = db.Column(db.Float, nullable=False, default=0.0)
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="employee")
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

    def __repr__(self) -> str:
        return f"<Employee id={self.id} user_id={self.user_id} rol={self.rol.value} active={self.is_active()}>"
