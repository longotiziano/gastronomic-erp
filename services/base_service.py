from typing import Generic, TypeVar
from sqlalchemy import inspect
from flask import request
from flask_sqlalchemy.pagination import Pagination

from database.repositories.base import BaseRepository
from utils.exceptions import ConflictError, NotFoundError, ValidationError, InternalError
from validators.base import BaseValidator

T = TypeVar("T")

class BaseCrudService(Generic[T]):
    def __init__(self, repo: BaseRepository[T]):
        self.repo = repo
        self.entity_name = getattr(self.repo.model, "entity_name", "registro")
        self.validator = BaseValidator(model=self.repo.model, repo=self.repo) # type: ignore


    def filter_sort(self) -> Pagination:
        search = ""
        filters = {}
        sorts = {}
        prefix = f"{self.repo.model.__tablename__}_" # type: ignore

        for key, value in request.args.items():
            print(f"Processing key: {key}, value: {value}")  # Debugging line
            if not key.startswith(prefix):
                print(f"Skipping key: {key} as it does not start with prefix: {prefix}")  # Debugging line
                continue
            
            stripped = key.removeprefix(prefix)

            if stripped == "search" and value:
                search = value
            elif stripped.startswith("filter_"):
                field = stripped.removeprefix("filter_")
                filters[field] = value
            elif stripped.startswith("sort_"):
                field = stripped.removeprefix("sort_")
                sorts[field] = (value == "desc")

        page = request.args.get(f"{prefix}page", 1, type=int)
        print(f"Search: {search}")
        return self.repo.get_filtered_sorted(
            search=search, filters=filters, sorts=sorts, page=page
        )


    def _get_table_rows(self, pagination: Pagination) -> list[dict]:
        """
        Returns a list of dictionaries representing the rows of the table.
        Each dictionary contains 'cells' and 'data' keys.
        """
        rows = []
        for item in pagination.items:
            if hasattr(item, "to_table_row"):
                cells = item.to_table_row()
            else:
                raise InternalError(f"El modelo {self.repo.model.__name__} debe implementar el método 'to_table_row()' para generar las celdas de la tabla.")
            
            data_payload = {}
            for column in inspect(self.repo.model).column_attrs: # type: ignore
                raw_val = getattr(item, column.key)
                # If the field is a SQLAlchemy Enum, store its plain string (.value)
                data_payload[column.key] = raw_val.value if hasattr(raw_val, "value") else raw_val
                
            rows.append({"cells": cells, "data": data_payload})
        return rows


    def get_table_metadata(self, pagination, is_main: bool = True) -> dict:
        """
        Builds the metadata required by Jinja using columns name list,
        instance cells method, and dumping all database attributes into data payload.
        """
        model = self.repo.model
        ui = getattr(model, "ui_config", {})
        if not ui:
            raise InternalError(f"El modelo {model.__name__} debe tener un atributo 'ui_config' para generar la tabla.")
        
        cols = ui.get("table_cols", [])
        rows = self._get_table_rows(pagination)

        # 3. Retornar la estructura exacta que Jinja consume
        return {
            "id": self.repo.model.__tablename__, # type: ignore
            "title": ui.get("title", self.entity_name.capitalize()),
            "cols": cols,
            "rows": rows,
            "form_template": ui.get("form_template"),
            "main_content": is_main,
            "secondary_content": not is_main,
            "pagination": pagination
        }


    def alt_status(self, entity_id: int) -> T:
        item = self.repo.get_by_id(entity_id)
        if not item:
            raise NotFoundError(f"{self.entity_name.capitalize()} no encontrada.")

        if not hasattr(item, "record_status"):
            raise ValidationError(f"{self.entity_name.capitalize()} no tiene el atributo 'record_status'.")

        new_status = not item.record_status # type: ignore
        updated = self.repo.update(entity_id, record_status=new_status)
        if not updated:
            raise ConflictError(f"No se pudo actualizar el estado de la {self.entity_name}.")

        return updated


    def create(self, **kwargs) -> T:
        """Dynamic function to create a record in the database."""
        if not kwargs:
            raise ValidationError("No se proporcionaron datos.")
        if kwargs.get("csrf_token"):
            del kwargs["csrf_token"]
        self.validator.validate(kwargs)

        result = self.repo.create(**kwargs)
        if result is None:
            raise ConflictError(f"No se ha podido crear el {self.entity_name}.")

        return result


    def update(self, entity_id: int, data: dict) -> T:
        """Dynamic function to update a record in the database."""
        if not data:
            raise ValidationError("No se proporcionaron datos.")
        if data.get("csrf_token"):
            del data["csrf_token"]
        self.validator.validate(data, check_required_fields=False, exclude_id=entity_id)

        result = self.repo.update(entity_id, **data)
        if result is None:
            raise ConflictError(f"No se ha podido actualizar la {self.entity_name} con ID {entity_id}.")

        return result