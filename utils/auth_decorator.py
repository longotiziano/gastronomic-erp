from functools import wraps

from flask import session

from services.bars import BarService
from database.models.user import UserRole
from database.repositories.users import UserRepository
from utils.exceptions import ForbiddenError, UnauthorizedError, NotFoundError
from utils.flashes import flash_message

def admin_required(f):
    """Validates a Flask session plus administrator privileges."""
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

from flask import redirect, url_for, g

def require_bar(f):
    """Sets the bar_id in the Flask's session. If the bar_id is None, then shows an error and redirects to `index.html`"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        bs = BarService()
        bars = bs.repo.get_all()
        bar_id = bs.get_session_bar(bars)
        if bar_id is None:
            if session.get("user_rol") == "administrator":
                flash_message("Error en la selección de bar",
                            "No se encuentran bares registrados. Crea uno para continuar.",
                            "warning")
            else:
                flash_message("Error en la selección de bar",
                            "No tenés un bar asignado. Por favor, contactá con algún administrador.",
                            "warning")
            return redirect(url_for("main.index"))
        g.bar_id = bar_id
        g.bars = {f"{b.name}": b.id for b in bars}
    return wrapper