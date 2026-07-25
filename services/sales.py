from database.models.sale import Sale
from database.repositories.sales import SaleRepository
from services.base_service import BaseCrudService
from utils.exceptions import ValidationError
from werkzeug.security import generate_password_hash
from utils.helpers import clean_string

import pandas as pd
from dataclasses import dataclass

@dataclass
class ParsedSaleRow:
    """Representa una fila cruda del informe de MaxiRest, sin resolver todavía
    contra la base de datos (no sabemos si el producto existe o no)."""
    product_name: str
    quantity: float
    total_amount: float

    @property
    def unit_price(self) -> float:
        """Precio aproximado por unidad."""
        if self.quantity == 0:
            return 0.0
        return round((self.total_amount / self.quantity), -3)


class SaleService(BaseCrudService):
    repo: SaleRepository
    
    
    def __init__(self):
        super().__init__(SaleRepository())
        self.required_columns = {"Nombre", "Unidad", "Importe"}


    def read_sales_excel(self, filepath: str) -> list[ParsedSaleRow]:
        """Reads MaxiRest's sales file and converts each row into a ParsedSaleRow."""
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            raise ValidationError("No se pudo leer el archivo. Verificá que sea un Excel válido.") from e

        df.columns = [str(col).strip().capitalize() for col in df.columns]
        missing_columns = self.required_columns - set(df.columns)
        if missing_columns:
            raise ValidationError(
                f"El archivo no tiene las columnas requeridas: {', '.join(sorted(missing_columns))}."
            )

        df = df[list(self.required_columns)].dropna(subset=list(self.required_columns))

        rows = []
        for _, row in df.iterrows():
            rows.append(ParsedSaleRow(
                product_name=str(row["Nombre"]).strip(),
                quantity=float(row["Unidad"]),
                total_amount=float(row["Importe"]),
            ))

        return rows


    def create(self, **data) -> Sale:


        return super().create(**data)
    

    def update(self, entity_id: int, data: dict) -> Sale:
            
        return super().update(entity_id, data)
    