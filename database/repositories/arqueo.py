from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.arqueo import Arqueo


class ArqueoRepository(BaseRepository[Arqueo]):
    model = Arqueo

    def get_by_bar(self, bar_id: int) -> list[Arqueo]:
        return (
            db.session.query(Arqueo)
            .filter_by(bar_id=bar_id)
            .order_by(Arqueo.created_at.desc())
            .all()
        )

    def get_by_date_range(self, bar_id: int, date_from: date, date_to: date) -> list[Arqueo]:
        return (
            db.session.query(Arqueo)
            .filter(
                Arqueo.bar_id == bar_id,
                Arqueo.created_at >= date_from,
                Arqueo.created_at <= date_to,
            )
            .order_by(Arqueo.created_at.desc())
            .all()
        )

    def get_by_cashier(self, cashier_id: int) -> list[Arqueo]:
        return db.session.query(Arqueo).filter_by(cashier_id=cashier_id).all()