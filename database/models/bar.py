from database import db
from datetime import datetime, timezone


class Bar(db.Model):
    __tablename__ = "bars"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    employees = db.relationship("Employee", back_populates="bar", lazy="dynamic")
    products = db.relationship("Product", back_populates="bar", lazy="dynamic")
    sales = db.relationship("Sale", back_populates="bar", lazy="dynamic")
    arqueos = db.relationship("Arqueo", back_populates="bar", lazy="dynamic")

    def __repr__(self):
        return f"<Bar id={self.id} name={self.name!r}>"