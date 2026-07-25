from datetime import datetime
from functools import cached_property
from typing import Any, Type, Dict, List
from sqlalchemy import Date, DateTime, inspect, Enum
from sqlalchemy.orm import Mapper, DeclarativeBase
from database import db
from utils.exceptions import ValidationError, ConflictError
from utils.helpers import clean_string


class BaseValidator:
    """
    Base Validator driven by SQLAlchemy model metadata.
    - model: The SQLAlchemy class model (e.g., RawMaterial)
    - repo: The repository instance to check database records (optional for basic field validation)
    """

    def __init__(self, model: Type[DeclarativeBase], repo: Any = None):
        self.model = model
        self.entity_name = getattr(model, "entity_name", "registro")
        self.repo = repo

    # =========================================================
    # ORQUESTADORES
    # =========================================================

    def validate(self, data: dict, check_required_fields: bool = True, exclude_id: int = None) -> None:  # type: ignore
        """
        Executes the full automated validation pipeline sequentially, for a single record.
        Modifies data dict in-place for text normalization.
        """
        self._normalize_date_fields(data)
        self._normalize_text_fields(data)

        if check_required_fields:
            self._validate_required_fields(data)

        if self.repo:
            self._validate_unique_fields(data, self.entity_name, exclude_id=exclude_id)
            self._validate_foreign_keys(data)

        self._validate_field_constraints(data)

    # =========================================================
    # METADATA (inspeccionada una sola vez por instancia, cacheada)
    # =========================================================

    @cached_property
    def _inspector(self) -> Mapper:
        return inspect(self.model)

    @cached_property
    def title_fields(self) -> List[str]:
        """Columnas que tienen 'title': True en su info."""
        return [
            column.key for column in self._inspector.column_attrs
            if (column.expression.info or {}).get("title") is True  # type: ignore
        ]

    @cached_property
    def date_fields(self) -> List[str]:
        """Columnas de tipo Date o DateTime."""
        return [
            column.name for column in self.model.__table__.columns
            if isinstance(column.type, (DateTime, Date))
        ]

    @cached_property
    def required_fields(self) -> List[str]:
        """Columnas NOT nullable, que no son PK, y sin default."""
        return [
            column.key for column in self._inspector.column_attrs
            if not column.expression.nullable  # type: ignore
            and not column.expression.primary_key  # type: ignore
            and column.expression.default is None  # type: ignore
        ]

    @cached_property
    def unique_fields(self) -> List[str]:
        """Columnas marcadas unique=True."""
        return [
            column.key for column in self._inspector.column_attrs
            if getattr(column.expression, 'unique', False)  # type: ignore
        ]

    @cached_property
    def fk_fields(self) -> Dict[str, Type[DeclarativeBase]]:
        """Mapa de columna local -> modelo remoto, para cada FK."""
        fk_relations = {}
        for rel in self._inspector.relationships:
            for col in rel.local_columns:
                if col.foreign_keys:
                    fk_relations[col.key] = rel.mapper.class_
        return fk_relations

    # =========================================================
    # NORMALIZERS (mutan data in-place)
    # =========================================================

    def _normalize_text_fields(self, data: dict) -> None:
        """Normaliza campos de texto (títulos) in-place."""
        for field in self.title_fields:
            if field in data and isinstance(data[field], str):
                data[field] = clean_string(data[field], title=True)

    def _normalize_date_fields(self, data: dict) -> None:
        """Convierte strings vacíos a None y strings con fecha a datetime, in-place."""
        for field in self.date_fields:
            if field not in data:
                continue

            value = data[field]

            if isinstance(value, str) and value.strip() == '':
                data[field] = None
                continue

            if isinstance(value, str):
                try:
                    data[field] = datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError(
                        f"El campo '{field}' no tiene un formato de fecha válido (YYYY-MM-DD)."
                    )

    # =========================================================
    # CHECKERS - individuales (validan y lanzan excepciones)
    # =========================================================

    def _validate_required_fields(self, data: dict) -> None:
        """Valida que los campos obligatorios estén presentes y no vacíos."""
        for field in self.required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == '':
                raise ValidationError(f"El campo '{field}' es obligatorio.")

    def _validate_unique_fields(self, data: dict, entity_name: str, exclude_id: int = None) -> None:  # type: ignore
        """Valida que los campos únicos no estén duplicados en el repositorio."""
        for field in self.unique_fields:
            if field in data and data[field] is not None:
                valor_a_chequear = data[field]
                if self.repo.record_exists(field, valor_a_chequear, exclude_id=exclude_id):
                    raise ConflictError(
                        f"Ya se encuentra registrado un {entity_name} con el valor "
                        f"'{valor_a_chequear}' en el campo '{field.capitalize()}'."
                    )

    def _validate_foreign_keys(self, data: dict) -> None:
        """Valida la integridad relacional de las claves foráneas."""
        for field, remote_model in self.fk_fields.items():
            if field in data and data[field] is not None:
                fk_value = data[field]
                if not self.repo.record_exists("id", fk_value, model=remote_model):
                    raise ValidationError(
                        f"El ID {fk_value} provisto para la relación '{field}' "
                        f"no corresponde a un registro existente."
                    )

    def _validate_field_constraints(self, data: dict) -> None:
        """Executes the pipeline of field's constraints (e.g. minimal values, enum types, string length...)"""
        for column_name, value in data.items():
            if value is None or str(value).strip() == '':
                continue
            self._check_enum(column_name, value)
            self._check_min_max_values(column_name, value)

    def _check_enum(self, column_name: str, value: Any) -> None:
        """Validates that the value belongs to the allowed options if the column is a SQLAlchemy Enum."""
        column_attr = self._inspector.column_attrs.get(column_name)
        if column_attr:
            col_type = column_attr.expression.type  # type: ignore
            if isinstance(col_type, Enum):
                if value not in col_type.enums:
                    raise ValidationError(
                        f"El valor '{value}' no es válido para el campo '{column_name}'. "
                        f"Opciones válidas: {', '.join(col_type.enums)}"
                    )

    def _check_min_max_values(self, column_name: str, value: Any) -> None:
        """Validates numeric ranges based on the column's info dictionary metadata (min_value / max_value)."""
        column_attr = self._inspector.column_attrs.get(column_name)
        if column_attr:
            col_info = column_attr.expression.info  # type: ignore
            min_value = col_info.get("min_value")
            max_value = col_info.get("max_value")

            if min_value is not None or max_value is not None:
                try:
                    valor_num = float(value)
                    if min_value is not None and valor_num < min_value:
                        raise ValidationError(f"El valor '{value}' es menor al mínimo permitido ({min_value}) para '{column_name}'.")
                    if max_value is not None and valor_num > max_value:
                        raise ValidationError(f"El valor '{value}' es mayor al máximo permitido ({max_value}) para '{column_name}'.")
                except (ValueError, TypeError):
                    raise ValidationError(f"El campo '{column_name}' debe recibir un valor numérico válido.")