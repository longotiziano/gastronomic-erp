from database import db
from datetime import datetime, timezone


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)          # Price at the moment of the sale
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    product = db.relationship("Product", back_populates="sales")
    bar = db.relationship("Bar", back_populates="sales")

    @property
    def subtotal(self) -> float:
        return self.amount * self.price

    def __repr__(self):
        return f"<Sale id={self.id} product_id={self.product_id} amount={self.amount} price={self.price}>"