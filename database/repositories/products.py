from database import db
from database.repositories.base import BaseRepository
from database.models.product import Product, ProductCategory, ProductSector


class ProductCategoryRepository(BaseRepository[ProductCategory]):
    model = ProductCategory


class ProductRepository(BaseRepository[Product]):
    model = Product