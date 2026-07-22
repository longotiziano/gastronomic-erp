from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.sale import Sale


class SaleRepository(BaseRepository[Sale]):
    model = Sale