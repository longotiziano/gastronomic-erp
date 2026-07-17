from database import db
from database.models.bar import Bar
from database.repositories.base import BaseRepository


class BarRepository(BaseRepository[Bar]):
    model = Bar

    def get_by_name(self, name: str) -> Bar | None:
        return db.session.query(Bar).filter_by(name=name).first()

    def bar_id_exists(self, bar_id: int) -> bool:
        return db.session.query(Bar).filter_by(id=bar_id).exists() is not None
