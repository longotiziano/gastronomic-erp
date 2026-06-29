from database import db


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    raw_material_id = db.Column(db.Integer, db.ForeignKey("raw_materials.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    uom = db.Column(db.String(20), nullable=False, default="gr")   # Unit of measure, e.g. gr, ml, unit

    # Relationships
    product = db.relationship("Product", back_populates="recipes")
    raw_material = db.relationship("RawMaterial", back_populates="recipes")

    def __repr__(self):
        return (
            f"<Recipe id={self.id} product_id={self.product_id} "
            f"raw_material_id={self.raw_material_id} amount={self.amount}{self.uom}>"
        )