from typing import Any


class BaseService:
    """Generic service layer with reusable CRUD and uniqueness checks."""

    def __init__(
        self,
        repository,
        *,
        check_existence: str | list[str] | None = None,
        existence_error_message: str | None = None,
    ):
        if repository is None:
            raise ValueError("A repository instance is required")

        self.repository = repository
        self.check_existence = check_existence
        self.existence_error_message = existence_error_message or "Ya existe un registro con el valor indicado"

    def _fields_to_check(self) -> list[str]:
        if self.check_existence is None:
            return []
        if isinstance(self.check_existence, str):
            return [self.check_existence]
        return list(self.check_existence)

    def _ensure_unique(self, data: dict[str, Any], *, exclude_id: int | None = None) -> None:
        for field in self._fields_to_check():
            if field not in data:
                continue
            value = data[field]
            if value is None:
                continue

            existing = self.repository.get_by_filter(**{field: value})
            if exclude_id is not None:
                existing = [item for item in existing if getattr(item, "id", None) != exclude_id]

            if existing:
                raise ValueError(f"{self.existence_error_message} ({field}={value})")

    def get_all(self, active_only: bool = True):
        return self.repository.get_all(active_only=active_only)

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def get_by_filter(self, **filters):
        return self.repository.get_by_filter(**filters)

    def create(self, **data):
        self._ensure_unique(data)
        return self.repository.create(**data)

    def update(self, id: int, **data):
        self._ensure_unique(data, exclude_id=id)
        return self.repository.update(id, **data)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
