from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from database.repositories import EmployeeRepository
from database.models.employee import EmployeeRole


def admin_required(f):
    """
    Decorator that validates:
      1. A valid JWT exists in the session cookie.
      2. The user linked to that JWT has an active employee record with the 'administrator' role.

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

        # 3. Look up the employee record linked to that user
        repo = EmployeeRepository()
        employee = repo.get_by_user(user_id)

        if employee is None:
            return jsonify({"error": "No employee record found for this user."}), 403

        if not employee.is_active:
            return jsonify({"error": "This employee is no longer active."}), 403

        if employee.rol != EmployeeRole.administrator:
            return jsonify({"error": "Administrator access required."}), 403

        return f(*args, **kwargs)

    return wrapper