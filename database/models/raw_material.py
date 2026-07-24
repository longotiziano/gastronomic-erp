import enum
from database import db


class Uom(enum.Enum):
    kg = "kg"
    gr = "gr"
    ml = "ml"
    l = "l"


class RawMaterialCategory(db.Model):
    __tablename__ = "raw_material_categories"
    entity_name = "categoría de materia prima"

    ui_config = {
        "title": "Categorías",
        "form_template": "forms/raw_categories_form.html",
        "table_cols": ["Nombre", "Estado"]
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, info={
        "title": True,
        "label": "Categoría",
        "filter_type": "search"
    })
    record_status = db.Column(db.Boolean, default=True, nullable=False, info={
        "label": "Estado",
        "filter_type": "bool"
    })

    # Relationships
    raw_materials = db.relationship("RawMaterial", back_populates="category", lazy="dynamic")

    def to_table_row(self) -> list:
        return [
            self.name,
            self.record_status
        ]

    def __repr__(self):
        return f"<RawMaterialCategory id={self.id} name={self.name!r}>"


class RawMaterial(db.Model):
    __tablename__ = "raw_materials"
    entity_name = "materia prima"

    ui_config = {
        "title": "Materias primas",
        "form_template": "forms/raw_materials_form.html",
        "table_cols": ["Nombre", "Categoría", "Unidad de Medida", "Estado"]
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True, info={
        "title": True,
        "label": "Materia Prima",
        "filter_type": "search"
    })
    category_id = db.Column(db.Integer, db.ForeignKey("raw_material_categories.id"), nullable=False, info={
        "label": "Categoría",
        "filter_type": "select_fk"
    })
    record_status = db.Column(db.Boolean, default=True, nullable=False, info={
        "label": "Estado",
        "filter_type": "bool"
    })
    uom = db.Column(db.Enum(Uom), nullable=False, default=Uom.gr, info={
        "label": "Unidad de Medida",
        "filter_type": "select"
    })

    filterable_fields = ["category_id", "record_status", "uom"]

    # Relationships
    category = db.relationship("RawMaterialCategory", back_populates="raw_materials")
    recipes = db.relationship("Recipe", back_populates="raw_material", lazy="dynamic")
    stock = db.relationship("Stock", back_populates="raw_material", uselist=False)
    stock_movements = db.relationship("StockMovement", back_populates="raw_material", lazy="dynamic")

    def to_table_row(self) -> list:
        """Devuelve exactamente las celdas que se van a dibujar en el HTML"""
        return [
            self.name,
            self.category.name if self.category else "-",
            self.uom.value if hasattr(self.uom, 'value') else self.uom,
            self.record_status
        ]

    def __repr__(self):
        return f"<RawMaterial id={self.id} name={self.name!r} active={self.record_status}>"