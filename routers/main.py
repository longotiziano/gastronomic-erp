from flask import Blueprint, render_template, session, request, redirect, url_for

from services.bars import BarService
from services.extras.dolar_service import get_cotizaciones_dolar
from utils.auth_decorator import admin_required
from utils.helpers import _get_saludo, _get_safe_next
from utils.flashes import flash_message
from utils.exceptions import ValidationError

main_bp = Blueprint("main", __name__)

bar_service = BarService()

@main_bp.route("/")
def index():
    rol = session.get("user_rol")
    is_logged = rol is not None
    if not is_logged:
        return redirect(url_for("auth.login"))
        
    is_admin = rol in ["administrator"] if rol else False
    
    bars = bar_service.repo.get_all()
    selected_bar_id = bar_service.get_session_bar(bars)
    selected_bar_name = session.get("bar_name")
    
    return render_template("index.html",
        user={
            "name": session.get("user_name", "Usuario"),
            "rol": rol
        },
        dolar=get_cotizaciones_dolar(),
        saludo=_get_saludo(),
        is_logged=is_logged,
        is_admin=is_admin,
        selected_bar_name = selected_bar_name,
        selected_bar_id = selected_bar_id,
        bar_selection={f"{b.name}": b.id for b in bars},
    )


@main_bp.post("/bar_selection")
@admin_required
def bar_select():
    safe_url = _get_safe_next()
    bar_id = request.form.get("bar_id", type=int)
    if not bar_id:
        raise ValidationError("No se ha proporcionado un bar.")

    bar_name = bar_service.get_bar_name(bar_id)
    session["bar_id"] = bar_id
    session["bar_name"] = bar_name
    flash_message("Cambio exitoso", f"Se ha cambiado el bar de trabajo a '{bar_name}'", "success")
    return redirect(safe_url)

    