import unittest

from app import create_app
from database import db
from services.bars import create_bar
from utils.exceptions import ConflictError, ValidationError


class BarsServiceTests(unittest.TestCase):
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

    def test_create_bar_requires_name(self):
        with self.assertRaises(ValidationError):
            create_bar("   ", "Calle 123")

    def test_create_bar_rejects_duplicate_name(self):
        create_bar("El Buen Sabor", "Calle 123")

        with self.assertRaises(ConflictError):
            create_bar("El Buen Sabor", "Calle 456")


if __name__ == "__main__":
    unittest.main()
