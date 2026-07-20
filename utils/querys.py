from sqlalchemy.orm import Query
from flask_sqlalchemy.pagination import Pagination

def _paginate_query(query: Query, page: int = 1, per_page: int = 20) -> Pagination:
    return query.paginate(page=page, per_page=per_page, error_out=False) # type: ignore