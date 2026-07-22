from database import db
from database.repositories.base import BaseRepository
from database.models.raw_material import RawMaterial, RawMaterialCategory


class RawMaterialCategoryRepository(BaseRepository[RawMaterialCategory]):
    model = RawMaterialCategory


class RawMaterialRepository(BaseRepository[RawMaterial]):
    model = RawMaterial