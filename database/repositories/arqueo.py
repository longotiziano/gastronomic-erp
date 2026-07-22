from datetime import date
from database import db
from database.repositories.base import BaseRepository
from database.models.arqueo import Arqueo


class ArqueoRepository(BaseRepository[Arqueo]):
    model = Arqueo