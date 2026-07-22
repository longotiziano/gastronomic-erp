import unittest

from app import create_app
from database import db
from data_seed import load_initial_data
from database.models.bar import Bar
from database.models.product import Product, ProductCategory
from database.models.raw_material import RawMaterial, RawMaterialCategory
from database.models.user import User


class DataSeedTests(unittest.TestCase):
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

    def test_load_initial_data_creates_seed_records(self):
        load_initial_data()

        bar = db.session.query(Bar).filter_by(name="Bar principal").first()
        self.assertIsNotNone(bar)

        admin_user = db.session.query(User).filter_by(email="admin@example.com").first()
        self.assertIsNotNone(admin_user)

        category = db.session.query(RawMaterialCategory).filter_by(name="Carnes").first()
        self.assertIsNotNone(category)

        raw_material = db.session.query(RawMaterial).filter_by(name="Carne picada").first()
        self.assertIsNotNone(raw_material)

        product_category = db.session.query(ProductCategory).filter_by(name="Bebidas").first()
        self.assertIsNotNone(product_category)

        product = db.session.query(Product).filter_by(name="Coca Cola").first()
        self.assertIsNotNone(product)


if __name__ == "__main__":
    unittest.main()
