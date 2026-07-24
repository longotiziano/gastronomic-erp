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
    entity_name = "usuario"

    ui_config = {
        "title": "Usuarios",
        "form_template": "forms/auth_form.html",
        "table_cols": ["Nombre", "Email", "Dirección", "Rol", "Salario Diario", "Bar", "Estado"]
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, info={
        "title": True,
        "filter_type": "search",
        "sort": True,
        "label": "Nombre"
    })
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, info={
        "min_length": 8
    })
    address = db.Column(db.String(255), nullable=True, info={
        "title": True,
        "label": "Dirección",
        "sort": True
    })
    rol = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.waiter, info={
        "filter_type": "select",
        "label": "Puesto",
        "sort": True
    })
    leave_at = db.Column(db.DateTime, nullable=True, info={
        "label": "Fecha de Despido",
        "sort": True
    })
    daily_salary = db.Column(db.Float, nullable=False, default=0.0, info={
        "min_value": 0.0,
        "label": "Salario diario",
        "sort": True
    })
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=True, info={
        "label": "Bar",
        "filter_type": "select_fk",
        "sort": True
    })
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, info={
        "label": "Fecha de creación",
        "sort": True
    })
    record_status = db.Column(db.Boolean, default=True, nullable=False, info={
        "label": "Estado",
        "filter_type": "bool",
        "sort": True
    })

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

    def to_table_row(self) -> list:
        return [
            self.name,
            self.email,
            self.address,
            self.rol.value if hasattr(self.rol, "value") else self.rol,
            f"${self.daily_salary:.2f}",
            self.bar.name if self.bar else "-",
            self.record_status,
        ]

    def is_active(self) -> bool:
        return self.leave_at is None

    def soft_delete(self) -> None:
        self.record_status = False

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} name={self.name!r} email={self.email!r} "
            f"role={self.rol.value if self.rol else None} active={self.is_active()}>"
        )
