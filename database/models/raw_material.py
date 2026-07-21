from database import db


class RawMaterialCategory(db.Model):
    __tablename__ = "raw_material_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    raw_materials = db.relationship("RawMaterial", back_populates="category", lazy="dynamic")

    def __repr__(self):
        return f"<RawMaterialCategory id={self.id} name={self.name!r}>"


class RawMaterial(db.Model):
    __tablename__ = "raw_materials"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("raw_material_categories.id"), nullable=False)
    record_status = db.Column(db.Boolean, default=True, nullable=False)
    uom = db.Column(db.String(20), nullable=False, default="gr")   # Unit of measure, e.g. gr, ml, unit

    filterable_fields = ["name", "category_id", "record_status", "uom"]

    # Relationships
    category = db.relationship("RawMaterialCategory", back_populates="raw_materials")
    recipes = db.relationship("Recipe", back_populates="raw_material", lazy="dynamic")
    stock = db.relationship("Stock", back_populates="raw_material", uselist=False)
    stock_movements = db.relationship("StockMovement", back_populates="raw_material", lazy="dynamic")

    def soft_delete(self) -> None:
        self.record_status = False

    def __repr__(self):
        return f"<RawMaterial id={self.id} name={self.name!r} active={self.record_status}>"