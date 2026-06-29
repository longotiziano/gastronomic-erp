import enum
from database import db


class ProductSector(enum.Enum):
    kitchen = "kitchen"
    bar = "bar"


class ProductCategory(db.Model):
    __tablename__ = "product_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.Enum(ProductSector), nullable=False)

    # Relationships
    products = db.relationship("Product", back_populates="category", lazy="dynamic")

    def __repr__(self):
        return f"<ProductCategory id={self.id} name={self.name!r} sector={self.sector.value}>"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("product_categories.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bar_id = db.Column(db.Integer, db.ForeignKey("bars.id"), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    category = db.relationship("ProductCategory", back_populates="products")
    bar = db.relationship("Bar", back_populates="products")
    sales = db.relationship("Sale", back_populates="product", lazy="dynamic")
    recipes = db.relationship("Recipe", back_populates="product", lazy="dynamic")

    def soft_delete(self) -> None:
        self.record_status = False

    def __repr__(self):
        return f"<Product id={self.id} name={self.name!r} price={self.price} active={self.record_status}>"