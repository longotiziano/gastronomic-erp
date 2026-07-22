from sqlalchemy.orm import Query
from flask_sqlalchemy.pagination import Pagination

def _paginate_query(query: Query, page: int = 1, per_page: int = 20) -> Pagination:
    "Receives a SQLAlchemy query, page and per_page and returns a Pagination object with the results."
    return query.paginate(page=page, per_page=per_page, error_out=False) # type: ignore