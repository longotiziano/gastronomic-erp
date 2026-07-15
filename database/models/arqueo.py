from database import db
from datetime import datetime, timezone


class Arqueo(db.Model):
    __tablename__ = "arqueos"

    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    card_total = db.Column(db.Float, nullable=False, default=0.0)
    cash_total = db.Column(db.Float, nullable=False, default=0.0)
    cash_difference = db.Column(db.Float, nullable=False, default=0.0)
    total_anulations = db.Column(db.Float, nullable=False, default=0.0)
    total_invitations = db.Column(db.Float, nullable=False, default=0.0)
    total_expenses = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=False)
    detail = db.Column(db.Text, nullable=True)
    arqueo_url = db.Column(db.String(500), nullable=True)   # URL or path to the generated PDF

    # Relationships
    cashier = db.relationship("User", foreign_keys=[cashier_id], back_populates="arqueos_as_cashier")
    manager = db.relationship("User", foreign_keys=[manager_id], back_populates="arqueos_as_manager")
    bar = db.relationship("Bar", back_populates="arqueos")

    def __repr__(self):
        return f"<Arqueo id={self.id} total={self.total} bar_id={self.bar_id} created_at={self.created_at}>"