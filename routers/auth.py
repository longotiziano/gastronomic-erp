from flask import Blueprint, render_template, request, session

from services.users import login_user, create_user

auth_bp = Blueprint("auth", __name__, )

@auth_bp.get("/auth/login")
def login():
    return render_template("auth/login.html")

@auth_bp.get("/auth/signup")
def signup():
    return render_template("auth/signup.html")

@auth_bp.post("/auth/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template("auth/login.html", error="Email y contraseña son requeridos")
    
    user = login_user(email, password)
    session["user_role"] = user.rol.value if user.rol else None
    session["user_id"] = user.id
    return render_template("index.html")

@auth_bp.post("/auth/signup")
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template("auth/signup.html", error="Email y contraseña son requeridos")
    
    user = create_user(name=request.form.get("name"), email=email, password=password)
    session["user_role"] = user.rol.value if user.rol else None
    session["user_id"] = user.id
    return render_template("index.html")

@auth_bp.post("/auth/logout")
def logout():
    # Implement logout logic here (e.g., clearing session, tokens, etc.)
    session.clear()
    return render_template("index.html")