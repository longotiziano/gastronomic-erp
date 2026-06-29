from database import db
from database.repositories.base import BaseRepository
from database.models.raw_material import RawMaterial, RawMaterialCategory


class RawMaterialCategoryRepository(BaseRepository[RawMaterialCategory]):
    model = RawMaterialCategory


class RawMaterialRepository(BaseRepository[RawMaterial]):
    model = RawMaterial

    def get_by_category(self, category_id: int, active_only: bool = True) -> list[RawMaterial]:
        query = db.session.query(RawMaterial).filter_by(category_id=category_id)
        if active_only:
            query = query.filter(RawMaterial.record_status == True)  # noqa: E712
        return query.all()