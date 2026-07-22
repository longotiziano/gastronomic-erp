from typing import Any, Type, Dict, List
from sqlalchemy import inspect, Enum
from sqlalchemy.orm import Mapper, DeclarativeBase
from utils.exceptions import ValidationError, ConflictError
from utils.helpers import clean_string

class BaseValidator:
    def __init__(self, model: Type[DeclarativeBase], repo: Any = None):
        """
        Base Validator driven by SQLAlchemy model metadata.
        - model: The SQLAlchemy class model (e.g., RawMaterial)
        - repo: The repository instance to check database records (optional for basic field validation)
        """
        self.model = model
        self.repo = repo

    def _obtain_title_fields(self) -> List[str]:
        """Inspecciona el modelo y devuelve las columnas que tienen 'title': True en su info."""
        inspector: Mapper = inspect(self.model)
        campos_titulo = []
        for column in inspector.column_attrs:
            col_info = column.expression.info or {} # type: ignore
            if col_info.get("title") is True:
                campos_titulo.append(column.key)
        return campos_titulo

    def _obtain_required_fields(self) -> List[str]:
        """Inspects the model and returns columns that are NOT nullable, NOT primary keys, and have NO default value."""
        inspector: Mapper = inspect(self.model)
        campos_obligatorios = []
        for column in inspector.column_attrs:
            col_prop = column.expression
            if not col_prop.nullable and not col_prop.primary_key and col_prop.default is None: # type: ignore
                campos_obligatorios.append(column.key)
        return campos_obligatorios

    def _obtain_unique_fields(self) -> List[str]:
        """Inspects the model and returns columns explicitly marked as unique=True."""
        inspector: Mapper = inspect(self.model)
        campos_unicos = []
        for column in inspector.column_attrs:
            col_prop = column.expression
            if getattr(col_prop, 'unique', False): # type: ignore
                campos_unicos.append(column.key)
        return campos_unicos

    def _obtain_fk_fields(self) -> Dict[str, Type[DeclarativeBase]]:
        """Inspects model relationships and returns a map of local column keys to their remote model classes."""
        inspector: Mapper = inspect(self.model)
        fk_relations = {}
        for rel in inspector.relationships:
            for col in rel.local_columns:
                if col.foreign_keys:
                    fk_relations[col.key] = rel.mapper.class_
        return fk_relations

    def _check_enum(self, column_name: str, value: Any) -> None:
        """Validates that the value belongs to the allowed options if the column is a SQLAlchemy Enum."""
        inspector: Mapper = inspect(self.model)
        column_attr = inspector.column_attrs.get(column_name)
        if column_attr:
            col_type = column_attr.expression.type # type: ignore
            if isinstance(col_type, Enum):
                if value not in col_type.enums:
                    raise ValidationError(
                        f"El valor '{value}' no es válido para el campo '{column_name}'. "
                        f"Opciones válidas: {', '.join(col_type.enums)}"
                    )

    def _check_min_max_values(self, column_name: str, value: Any) -> None:
        """Validates numeric ranges based on the column's info dictionary metadata (min_value / max_value)."""
        inspector: Mapper = inspect(self.model)
        column_attr = inspector.column_attrs.get(column_name)
        if column_attr:
            col_info = column_attr.expression.info # type: ignore
            min_value = col_info.get("min_value")
            max_value = col_info.get("max_value")
            
            # Si el tipo amerita comparación numérica, intentamos castearlo para evitar crashes
            if min_value is not None or max_value is not None:
                try:
                    valor_num = float(value)
                    if min_value is not None and valor_num < min_value:
                        raise ValidationError(f"El valor '{value}' es menor al mínimo permitido ({min_value}) para '{column_name}'.")
                    if max_value is not None and valor_num > max_value:
                        raise ValidationError(f"El valor '{value}' es mayor al máximo permitido ({max_value}) para '{column_name}'.")
                except (ValueError, TypeError):
                    raise ValidationError(f"El campo '{column_name}' debe recibir un valor numérico válido.")

    def validate(self, data: dict, entity_name: str = "registro", check_required_fields: bool = True) -> None:
        """
        Executes the full automated validation pipeline sequentially.
        Modifies data dict in-place for text normalization.
        """
        for field in self._obtain_title_fields():
            if field in data and isinstance(data[field], str):
                data[field] = clean_string(data[field], title=True)

        # 1. Validación de campos obligatorios (Ya leerá el texto limpio sin espacios locos)
        if check_required_fields:
            for field in self._obtain_required_fields():
                if field not in data or data[field] is None or str(data[field]).strip() == '':
                    raise ValidationError(f"El campo '{field}' es obligatorio.")

        if self.repo:
            # 2. Validación de duplicados (Campos Únicos)
            # 🚀 ¡OJO! Al haber normalizado el texto arriba, la query 'record_exists' 
            # buscará "Harina 000" de forma exacta, previniendo duplicados reales de tipeo.
            for field in self._obtain_unique_fields():
                if field in data and data[field] is not None:
                    valor_a_chequear = data[field]
                    if self.repo.record_exists(field, valor_a_chequear):
                        raise ConflictError(
                            f"Ya se encuentra registrado un {entity_name} con el valor '{valor_a_chequear}' en el campo '{field.capitalize()}'."
                        )

            # 3. Validación de integridad relacional (Claves Foráneas)
            for field, remote_model in self._obtain_fk_fields().items():
                if field in data and data[field] is not None:
                    fk_value = data[field]
                    if not self.repo.record_exists("id", fk_value, model=remote_model):
                        raise ValidationError(
                            f"El ID {fk_value} provisto para la relación '{field}' no corresponde a un registro existente."
                        )

        # 4. Pipeline de restricciones específicas campo por campo
        for column_name, value in data.items():
            if value is None or str(value).strip() == '':
                continue
            self._check_enum(column_name, value)
            self._check_min_max_values(column_name, value)