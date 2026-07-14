from database import db
from database.repositories.base import BaseRepository
from database.models.stock import Stock, StockMovement, MovementType


class StockRepository(BaseRepository[Stock]):
    model = Stock

    def get_by_raw_material(self, raw_material_id: int) -> Stock | None:
        return db.session.query(Stock).filter_by(raw_material_id=raw_material_id).first()


class StockMovementRepository(BaseRepository[StockMovement]):
    model = StockMovement

    def get_by_raw_material(self, raw_material_id: int) -> list[StockMovement]:
        return (
            db.session.query(StockMovement)
            .filter_by(raw_material_id=raw_material_id)
            .order_by(StockMovement.created_at.desc())
            .all()
        )

    def get_by_type(self, movement_type: MovementType) -> list[StockMovement]:
        return db.session.query(StockMovement).filter_by(type=movement_type).all()