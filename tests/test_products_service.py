import unittest

from app import create_app
from database import db
from services.bars import create_bar
from services.products import create_product, create_product_category
from utils.exceptions import ValidationError


class ProductsServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.testing = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_product_category_requires_name(self):
        with self.assertRaises(ValidationError):
            create_product_category("   ", "kitchen")

    def test_create_product_requires_positive_price(self):
        bar = create_bar("Bar test", "Calle 123")
        category = create_product_category("Bebidas", "bar")

        with self.assertRaises(ValidationError):
            create_product("Coca Cola", category.id, -5, bar.id)


if __name__ == "__main__":
    unittest.main()
