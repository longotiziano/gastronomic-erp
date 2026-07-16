from flask import Blueprint, render_template, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    rol = session.get("user_role")
    is_logged = rol is not None
    is_admin = rol in ["administrator"] if rol else False
    if is_logged:
        print(f"User is logged in with role: {rol}")
    return render_template("index.html", is_logged=is_logged, is_admin=is_admin)