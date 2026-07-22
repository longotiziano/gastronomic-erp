from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy.pagination import Pagination
from typing import Generic, TypeVar, Type, Optional
from database import db
from sqlalchemy import or_

from utils.exceptions import ConflictError
from utils.querys import _paginate_query

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Generic base repository. Each model repository inherits from this class
    passing its model as the type parameter.

    Usage:
        class UserRepository(BaseRepository[User]):
            model = User
    """

    model: Type[T]

    # ------------------------------------------------------------------ #
    #  Read                                                                #
    # ------------------------------------------------------------------ #

    def get_by_id(self, id: int) -> Optional[T]:
        """Return a single record by primary key, or None if not found."""
        return db.session.get(self.model, id)

    def record_exists(self, col_name: str, check_value, exclude_id: Optional[int] = None, model=None) -> bool:
        if model is None:
            model = self.model

        column = getattr(model, col_name)
        query = db.session.query(model).filter(column == check_value)
        if exclude_id is not None and hasattr(model, "id"):
            query = query.filter(model.id != exclude_id) # type: ignore
        return db.session.query(query.exists()).scalar()
    
    def get_all(self, active_only: bool = True) -> list[T]:
        """
        Return all records.
        If the model has record_status, filter by active records by default.
        """
        query = db.session.query(self.model)
        if active_only and hasattr(self.model, "record_status"):
            query = query.filter(self.model.record_status == True)  # noqa: E712 # type: ignore
        return query.all()

    def get_filtered_sorted(
        self,
        search: str = "",
        filters: dict = None, # type: ignore
        sorts: dict = None, # type: ignore
        page: int = 1,
        per_page: int = 20
    ) -> Pagination:
        filters = filters or {}
        sorts = sorts or {}
        allowed = getattr(self.model, "filterable_fields", set())

        query = db.session.query(self.model)

        if search:
            search_conditions = [
                getattr(self.model, field).ilike(f"%{search}%")
                for field in allowed
            ]
            if search_conditions:
                query = query.filter(or_(*search_conditions))

        for k, v in filters.items():
            if k not in allowed:
                continue
            query = query.filter(getattr(self.model, k) == v)

        for field, descending in sorts.items():
            if field not in allowed:
                continue
            column = getattr(self.model, field)
            query = query.order_by(column.desc() if descending else column.asc())

        return _paginate_query(query, page, per_page) # type: ignore

    def get_by_filter(self, **filters) -> list[T]:
        """
        Return records matching all keyword filters.

        Example:
            repo.get_by_filter(bar_id=1, record_status=True)
        """
        query = db.session.query(self.model)
        for attr, value in filters.items():
            query = query.filter(getattr(self.model, attr) == value)
        return query.all()

    def paginate(self, page: int = 1, per_page: int = 20, active_only: bool = True):
        """
        Return a SQLAlchemy Pagination object.

        Usage:
            pagination = repo.paginate(page=2, per_page=10)
            records     = pagination.items
            total_pages = pagination.pages
        """
        query = db.session.query(self.model)
        if active_only and hasattr(self.model, "record_status"):
            query = query.filter(self.model.record_status == True)  # noqa: E712 # type: ignore
        return _paginate_query(query, page=page, per_page=per_page) # type: ignore

    # ------------------------------------------------------------------ #
    #  Write                                                               #
    # ------------------------------------------------------------------ #

    def create(self, **kwargs) -> T:
        """
        Instantiate, persist, and return a new record.

        Raises:
            ConflictError: if a unique/foreign key constraint is violated.
        """
        instance = self.model(**kwargs)
        db.session.add(instance)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ConflictError("El registro ya existe o viola una restricción.") from e
        db.session.refresh(instance)
        return instance

    def update(self, id: int, **kwargs) -> Optional[T]:
        """
        Update fields on an existing record and return it.
        Returns None if the record does not exist.
        """
        instance = self.get_by_id(id)
        if instance is None:
            return None
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        db.session.commit()
        db.session.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        """
        Soft-delete a record if it has record_status, otherwise raise.
        Returns True on success, False if the record was not found.
        """
        instance = self.get_by_id(id)
        if instance is None:
            return False
        if not hasattr(instance, "record_status"):
            raise NotImplementedError(
                f"{self.model.__name__} does not support soft delete (no record_status column). "
                "Override delete() in the concrete repository if physical deletion is needed."
            )
        instance.record_status = False # type: ignore
        db.session.commit()
        return True