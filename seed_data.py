from app import create_app
from database import db
import database.models  # noqa: F401 - register all models
from database.models.bar import Bar
from database.models.user import User
from database.models.employee import Employee, EmployeeRole
from database.models.product import ProductCategory, Product, ProductSector
from database.models.raw_material import RawMaterialCategory, RawMaterial
from database.models.recipe import Recipe
from database.models.stock import Stock


def get_or_create(model, defaults=None, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    params = {**kwargs}
    if defaults:
        params.update(defaults)
    instance = model(**params)
    db.session.add(instance)
    db.session.flush()
    return instance


def seed_data():
    app = create_app()
    with app.app_context():
        # Bar
        bar = get_or_create(Bar, name="La Cocina Central")

        # User + employee
        user = get_or_create(
            User,
            defaults={"name": "Admin Demo", "password": "hashed-password-demo"},
            email="admin@example.com",
        )
        if not user.name:
            user.name = "Admin Demo"
        if not user.password:
            user.password = "hashed-password-demo"

        employee = db.session.query(Employee).filter_by(user_id=user.id).first()
        if not employee:
            employee = Employee(
                user_id=user.id,
                address="Av. Siempre Viva 123",
                rol=EmployeeRole.administrator,
                daily_salary=1500.0,
                bar_id=bar.id,
            )
            db.session.add(employee)

        # Product categories
        category_food = get_or_create(
            ProductCategory,
            defaults={"sector": ProductSector.kitchen},
            name="Platos",
        )
        category_drink = get_or_create(
            ProductCategory,
            defaults={"sector": ProductSector.bar},
            name="Bebidas",
        )

        # Products
        products_data = [
            {"name": "Milanesa con papas", "category_id": category_food.id, "price": 1800.0},
            {"name": "Cerveza artesanal", "category_id": category_drink.id, "price": 1200.0},
        ]
        for data in products_data:
            existing = db.session.query(Product).filter_by(name=data["name"]).first()
            if not existing:
                db.session.add(
                    Product(
                        name=data["name"],
                        category_id=data["category_id"],
                        price=data["price"],
                        bar_id=bar.id,
                    )
                )

        # Raw materials and stock
        raw_category = get_or_create(RawMaterialCategory, name="Carnes")
        raw_material = db.session.query(RawMaterial).filter_by(name="Carne vacuna").first()
        if not raw_material:
            raw_material = RawMaterial(name="Carne vacuna", category_id=raw_category.id)
            db.session.add(raw_material)

        stock = db.session.query(Stock).filter_by(raw_material_id=raw_material.id).first()
        if not stock:
            db.session.add(Stock(raw_material_id=raw_material.id, amount=25.0))

        db.session.commit()
        print("Datos de prueba cargados correctamente.")


if __name__ == "__main__":
    seed_data()
