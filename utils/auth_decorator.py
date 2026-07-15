from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from database.models.user import UserRole
from database.repositories.users import UserRepository


def admin_required(f):
    """
    Decorator that validates:
      1. A valid JWT exists in the session cookie.
      2. The user linked to that JWT is active and has the 'administrator' role.

    Usage:
        @app.route("/admin/dashboard")
        @admin_required
        def dashboard():
            ...
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 1. Verify JWT presence and signature (raises exception if invalid/missing)
        try:
            verify_jwt_in_request(locations=["cookies"])
        except Exception:
            return jsonify({"error": "Authentication required."}), 401

        # 2. Get user_id from token payload
        user_id = get_jwt_identity()

        # 3. Look up the unified user record linked to that ID
        repo = UserRepository()
        user = repo.get_by_id(user_id)

        if user is None:
            return jsonify({"error": "No user record found."}), 403

        if not user.is_active():
            return jsonify({"error": "This user is no longer active."}), 403

        if user.rol != UserRole.administrator:
            return jsonify({"error": "Administrator access required."}), 403

        return f(*args, **kwargs)

    return wrapper