from flask import Blueprint, redirect, render_template, request, session, url_for

from services.users import login_user

auth_bp = Blueprint("auth", __name__, )

@auth_bp.get("/auth/login")
def login():
    return render_template("auth/login.html", **_login_context())

@auth_bp.post("/auth/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template("auth/login.html", 
            error="Email y contraseña son requeridos",
            **_login_context()
        )
    
    user = login_user(email, password)
    if not user:
        return render_template("auth/login.html",
            error="Credenciales inválidas",
            **_login_context()
        )
    
    session["user_role"] = user.rol.value if user.rol else None
    session["user_id"] = user.id
    return redirect(url_for("main.index"))

@auth_bp.post("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))

def _login_context():
    return {
        "title": "Iniciar sesión",
        "form_action": url_for('auth.login_post'),
        "submit_text": "Iniciar sesión",
        "is_modal": False
    }