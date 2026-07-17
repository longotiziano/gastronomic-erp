from database import db
from database.models.bar import Bar
from database.repositories.base import BaseRepository


class BarRepository(BaseRepository[Bar]):
    model = Bar

    def get_by_name(self, name: str) -> Bar | None:
        return db.session.query(Bar).filter_by(name=name).first()

    def get_by_name_case_insensitive(self, name: str) -> Bar | None:
        normalized_name = name.strip().lower()
        return db.session.query(Bar).filter(db.func.lower(Bar.name) == normalized_name).first()

    def bar_id_exists(self, bar_id: int) -> bool:
        return db.session.query(Bar).filter_by(id=bar_id).exists() is not None
