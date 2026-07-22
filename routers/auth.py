from flask import Blueprint, redirect, render_template, request, session, url_for

from services.users import UserService
from utils.flashes import flash_message

auth_bp = Blueprint("auth", __name__, )
user_service = UserService()

@auth_bp.get("/auth/login")
def login():
    return _login_context()

@auth_bp.post("/auth/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        flash_message("Error en el inicio de sesión", "Email y contraseña son requeridos", "error")
        return _login_context()
    
    user = user_service.login(email, password)
    if not user:
        flash_message("Error en el inicio de sesión", "Email o contraseña incorrectos", "error")
        return _login_context()
    
    session["user_role"] = user.rol.value if user.rol else None
    session["user_id"] = user.id
    return redirect(url_for("main.index"))

@auth_bp.post("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))

def _login_context() -> str:
    return render_template("sections/login.html",
        form_title= "Iniciar sesión",
        form_action=url_for('auth.login_post'),
        submit_text="Iniciar sesión",
        is_modal=False
    )