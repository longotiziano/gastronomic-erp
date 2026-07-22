import enum
from database import db


class ProductSector(enum.Enum):
    kitchen = "kitchen"
    bar = "bar"


class ProductCategory(db.Model):
    __tablename__ = "product_categories"
    entity_name = "categoría de producto"

    ui_config = {
        "title": "Categorías",
        "form_template": "forms/product_categories_form.html",
        "table_cols": ["Nombre", "Sector", "Estado"]
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, info={
        "title": True
    })
    sector = db.Column(db.Enum(ProductSector), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)

    filterable_fields = ["name", "sector", "record_status"]

    # Relationships
    products = db.relationship("Product", back_populates="category", lazy="dynamic")

    def to_table_row(self) -> list:
        return [
            self.name,
            self.sector.value if hasattr(self.sector, "value") else self.sector,
            self.record_status,
        ]

    def __repr__(self):
        return f"<ProductCategory id={self.id} name={self.name!r} sector={self.sector.value}>"


class Product(db.Model):
    __tablename__ = "products"
    entity_name = "producto"

    ui_config = {
        "title": "Productos",
        "form_template": "forms/products_form.html",
        "table_cols": ["Nombre", "Categoría", "Precio", "Bar", "Estado"]
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, info={
        "title": True
    })
    category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"), nullable=False)
    price = db.Column(db.Float, nullable=False, info={
        "min_value": 0.0
    })
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)

    filterable_fields = ["name", "category_id", "bar_id", "record_status"]

    # Relationships
    category = db.relationship("ProductCategory", back_populates="products")
    bar = db.relationship("Bar", back_populates="products")
    sales = db.relationship("Sale", back_populates="product", lazy="dynamic")
    recipes = db.relationship("Recipe", back_populates="product", lazy="dynamic")

    def to_table_row(self) -> list:
        return [
            self.name,
            self.category.name if self.category else "-",
            self.price,
            self.bar.name if self.bar else "-",
            self.record_status,
        ]

    def soft_delete(self) -> None:
        self.record_status = False

    def __repr__(self):
        return f"<Product id={self.id} name={self.name!r} price={self.price} active={self.record_status}>"