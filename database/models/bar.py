from database import db
from datetime import datetime, timezone


class Bar(db.Model):
    __tablename__ = "bars"
    entity_name = "bar"
    
    ui_config = {
        "title": "Bares",
        "form_template": "forms/bars_form.html",
        "table_cols": ["Nombre", "Dirección", "Fecha de creación", "Estado"]
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, info={
        "title": True
    })
    address = db.Column(db.String(255), nullable=True, info={
        "title": True
    })
    record_status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    employees = db.relationship("User", back_populates="bar", lazy="dynamic")
    stock = db.relationship("Stock", back_populates="bar", lazy="dynamic")
    products = db.relationship("Product", back_populates="bar", lazy="dynamic")
    sales = db.relationship("Sale", back_populates="bar", lazy="dynamic")
    arqueos = db.relationship("Arqueo", back_populates="bar", lazy="dynamic")

    def to_table_row(self) -> list:
        return [
            self.name,
            self.address or "-",
            self.created_at.strftime("%d-%m-%Y") if self.created_at else "-",
            self.record_status,
        ]

    def __repr__(self):
        return f"<Bar id={self.id} name={self.name!r} address={self.address!r}>"