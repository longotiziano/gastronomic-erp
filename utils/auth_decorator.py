from functools import wraps

from flask import jsonify, session

from database.models.user import UserRole
from database.repositories.users import UserRepository
from utils.exceptions import ForbiddenError, UnauthorizedError, NotFoundError

def admin_required(f):
    """
    Decorator that validates a Flask session plus administrator privileges.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            raise UnauthorizedError()

        repo = UserRepository()
        user = repo.get_by_id(user_id)

        if user is None:
            session.clear()
            raise NotFoundError("No se han encontrado usuarios activos con este ID. Por favor, contacte al administrador del sistema.")

        if not user.is_active():
            session.clear()
            raise ForbiddenError("Tu cuenta se encuentra desactivada. Por favor, contacta al administrador del sistema.")

        if user.rol != UserRole.administrator:
            raise ForbiddenError()

        return f(*args, **kwargs)

    return wrapper