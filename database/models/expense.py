from database import db
from datetime import datetime, timezone


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(50), nullable=False)   # e.g. 'cash', 'card', 'transfer'
    amount = db.Column(db.Float, nullable=False)
    detail = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Expense id={self.id} payment_type={self.payment_type!r} amount={self.amount}>"