import enum
from database import db
from datetime import datetime, timezone


class MovementType(enum.Enum):
    in_ = "in"
    out = "out"


class Stock(db.Model):
    """Current stock level for a raw material. One record per raw material."""

    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    raw_material_id = db.Column(
        db.Integer, db.ForeignKey("raw_materials.id"), unique=True, nullable=False
    )
    amount = db.Column(db.Float, nullable=False, default=0.0)

    # Relationships
    raw_material = db.relationship("RawMaterial", back_populates="stock")

    def __repr__(self):
        return f"<Stock id={self.id} raw_material_id={self.raw_material_id} amount={self.amount}>"


class StockMovement(db.Model):
    """Audit log of every stock change (incoming deliveries or consumption)."""

    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)
    raw_material_id = db.Column(db.Integer, db.ForeignKey("raw_materials.id"), nullable=False)
    type = db.Column(db.Enum(MovementType), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    raw_material = db.relationship("RawMaterial", back_populates="stock_movements")

    def __repr__(self):
        return (
            f"<StockMovement id={self.id} raw_material_id={self.raw_material_id} "
            f"type={self.type.value} amount={self.amount}>"
        )