from database import db
from datetime import datetime, timezone, date


class Payroll(db.Model):
    __tablename__ = "payrolls"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    day = db.Column(db.Date, nullable=False)                        # The worked day being paid
    amount = db.Column(db.Float, nullable=False)
    received_by_employee = db.Column(db.DateTime, nullable=False)   # When the employee received the payment
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    employee = db.relationship("Employee", back_populates="payrolls")

    def __repr__(self):
        return f"<Payroll id={self.id} employee_id={self.employee_id} day={self.day} amount={self.amount}>"