from typing import Generic, TypeVar, Any, Optional
from database.repositories.base import BaseRepository
from utils.exceptions import ConflictError, NotFoundError, ValidationError

T = TypeVar("T")


class BaseCrudService(Generic[T]):
    def __init__(self, repo: BaseRepository[T], entity_name: str = "entidad"):
        self.repo = repo
        self.entity_name = entity_name

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

    def update(self, entity_id: int, processed_updates: dict, field_existence: Optional[dict[str, Any]] = None) -> T:
        if not processed_updates:
            raise ValidationError("No hay campos válidos para actualizar")

        field_existence = field_existence or {}
        for k, v in field_existence.items():
            if self.repo.record_exists(k, v, exclude_id=entity_id):
                raise ConflictError(
                    f"Ya se encuentra registrado un {self.entity_name} con el valor {v} en el campo {k.capitalize()}."
                )

        result = self.repo.update(entity_id, **processed_updates)
        if result is None:
            raise ConflictError(f"No se ha podido actualizar la {self.entity_name} con ID {entity_id}.")

        return result
    
    def create(self, field_existence: Optional[dict[str, Any]] = None, **kwargs) -> T:
        """
        En caso de proveerse el parámetro field_existence en forma {nombre_col: valor} se chequea que
        en nombre_col NO exista el valor introducido
        """
        field_existence = field_existence or {}

        for k, v in field_existence.items():
            if self.repo.record_exists(k, v):
                raise ConflictError(
                    f"Ya se encuentra registrado un {self.entity_name} con el valor {v} en el campo {k.capitalize()}."
                )

        result = self.repo.create(**kwargs)
        if result is None:
            raise ConflictError(f"No se ha podido crear el {self.entity_name}.")

        return result