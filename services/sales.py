from database.models.sale import Sale
from database.models.product import Product
from database.repositories.sales import SaleRepository
from services.base_service import BaseCrudService
from utils.exceptions import ValidationError

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
        """Reads MaxiRest's sales file and converts each row into a ParsedSaleRow. Checks duplicates"""
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
        df["Nombre"] = df["Nombre"].astype(str).str.strip()

        duplicated_mask = df["Nombre"].duplicated(keep=False)
        if duplicated_mask.any():
            duplicated_names = sorted(df.loc[duplicated_mask, "Nombre"].unique())
            raise ValidationError(
                f"El archivo contiene productos duplicados: {', '.join(duplicated_names)}."
            )

        rows = []
        for _, row in df.iterrows():
            rows.append(ParsedSaleRow(
                product_name=row["Nombre"],
                quantity=float(row["Unidad"]),
                total_amount=float(row["Importe"]),
            ))

        return rows


    def check_missing_products(self, rows_list: list[ParsedSaleRow]) -> list[ParsedSaleRow]:
        """Receives a list of ParsedSaleRow, and returns the registers that are NOT in database"""
        product_names = [r.product_name for r in rows_list]
        missing_products = self.repo.values_not_present_in("name", product_names, model=Product)
        parsed_list = [r for r in rows_list if r.product_name in missing_products]
        return parsed_list


    def create(self, **data) -> Sale:


        return super().create(**data)
    

    def update(self, entity_id: int, data: dict) -> Sale:
            
        return super().update(entity_id, data)
    