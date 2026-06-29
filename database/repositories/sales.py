from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.sale import Sale


class SaleRepository(BaseRepository[Sale]):
    model = Sale

    def get_by_bar(self, bar_id: int) -> list[Sale]:
        return db.session.query(Sale).filter_by(bar_id=bar_id).all()

    def get_by_date_range(self, bar_id: int, date_from: date, date_to: date) -> list[Sale]:
        return (
            db.session.query(Sale)
            .filter(
                Sale.bar_id == bar_id,
                Sale.created_at >= date_from,
                Sale.created_at <= date_to,
            )
            .all()
        )

    def get_by_product(self, product_id: int) -> list[Sale]:
        return db.session.query(Sale).filter_by(product_id=product_id).all()