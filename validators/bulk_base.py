from typing import List, Any
from validators.base import BaseValidator
from database.repositories.base import BaseRepository
from utils.exceptions import ValidationError, ConflictError


class BulkValidator(BaseValidator):

    repo: BaseRepository

    # =========================================================
    # ORQUESTADOR
    # =========================================================

    def bulk_validate(self, data_list: List[dict]) -> None:
        """
        Valida un lote de registros de forma eficiente:
        - Normaliza y valida campos obligatorios/constraints fila por fila (sin acceso a DB).
        - Resuelve unique y FK con una sola query por campo para todo el lote.
        Acumula todos los errores encontrados y los lanza juntos al final.
        """
        errores: List[str] = []

        for i, data in enumerate(data_list):
            try:
                self._normalize_date_fields(data)
                self._normalize_text_fields(data)
                self._validate_required_fields(data)
                self._validate_field_constraints(data)
            except (ValidationError, ConflictError) as e:
                errores.append(f"Fila {i + 1}: {e}")

        if self.repo:
            errores.extend(self._bulk_check_unique_fields(data_list))
            errores.extend(self._bulk_check_fk_fields(data_list))

        if errores:
            raise ValidationError("Se encontraron errores en el archivo:\n" + "\n".join(errores))

    # =========================================================
    # CAMPOS ÚNICOS (dentro del lote + contra la base)
    # =========================================================

    def _bulk_check_unique_fields(self, data_list: List[dict]) -> List[str]:
        """Valida que los campos únicos no tengan conflictos, dentro del lote y contra la base."""
        errores: List[str] = []

        for field in self.unique_fields:
            valores_en_lote = [d[field] for d in data_list if d.get(field) is not None]
            if not valores_en_lote:
                continue

            errores.extend(self._check_duplicates_within_batch(field, valores_en_lote))
            errores.extend(self._check_duplicates_against_db(field, valores_en_lote))

        return errores

    def _check_duplicates_within_batch(self, field: str, values: List[Any]) -> List[str]:
        """Detecta valores repetidos dentro del propio lote (mismo archivo cargado)."""
        errores = []
        vistos = set()
        for valor in values:
            if valor in vistos:
                errores.append(f"Valor duplicado '{valor}' en el campo '{field}' dentro del archivo.")
            vistos.add(valor)
        return errores

    def _check_duplicates_against_db(self, field: str, values: List[Any]) -> List[str]:
        """Detecta valores que ya existen en la base de datos, para todo el lote de una vez."""
        existentes = self.repo.values_present_in(field, values)
        return [
            f"Ya existe un {self.entity_name} con el valor '{valor}' en el campo '{field}'."
            for valor in existentes
        ]

    # =========================================================
    # CLAVES FORÁNEAS (contra la base)
    # =========================================================

    def _bulk_check_fk_fields(self, data_list: List[dict]) -> List[str]:
        """Valida que los IDs de FK provistos existan en la base, para todo el lote de una vez."""
        errores: List[str] = []

        for field, remote_model in self.fk_fields.items():
            valores_en_lote = {d[field] for d in data_list if d.get(field) is not None}
            if not valores_en_lote:
                continue

            errores.extend(self._check_fk_exists(field, remote_model, valores_en_lote))

        return errores

    def _check_fk_exists(self, field: str, remote_model, valores: set) -> List[str]:
        """Detecta IDs que no existen en el modelo remoto, para un campo FK puntual."""
        existentes = self.repo.values_present_in("id", list(valores), model=remote_model)
        faltantes = valores - existentes
        return [
            f"El ID {valor} provisto para la relación '{field}' no corresponde a un registro existente."
            for valor in faltantes
        ]