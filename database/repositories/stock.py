from database import db
from database.repositories.base import BaseRepository
from database.models.stock import Stock, StockMovement, MovementType


class StockRepository(BaseRepository[Stock]):
    model = Stock


class StockMovementRepository(BaseRepository[StockMovement]):
    model = StockMovement