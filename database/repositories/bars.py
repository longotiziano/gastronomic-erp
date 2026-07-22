from database import db
from database.models.bar import Bar
from database.repositories.base import BaseRepository


class BarRepository(BaseRepository[Bar]):
    model = Bar