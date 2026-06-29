import traceback
from flask import Flask, jsonify
from exceptions import (
    AppException,
    ValidationError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    InternalError,
)

# ANSI color codes for console output
_RESET  = "\033[0m"
_RED    = "\033[31m"
_YELLOW = "\033[33m"
_CYAN   = "\033[36m"
_BOLD   = "\033[1m"

_STATUS_COLORS = {
    400: _YELLOW,
    401: _YELLOW,
    403: _YELLOW,
    404: _CYAN,
    409: _YELLOW,
    500: _RED,
}


def _log(app: Flask, e: AppException) -> None:
    """Print a formatted error to the console when DEBUG mode is on."""
    if not app.debug:
        return
    color = _STATUS_COLORS.get(e.status_code, _RESET)
    app.logger.debug(
        "%s%s[%d] %s — %s%s",
        _BOLD, color,
        e.status_code,
        type(e).__name__,
        e.message,
        _RESET,
    )
    # Full traceback so the exact raise location is visible
    traceback.print_exc()


def register_error_handlers(app: Flask) -> None:
    """
    Register all custom exception handlers on the Flask app.
    Call this inside create_app() after initializing extensions.

    Usage in app.py:
        from errors import register_error_handlers
        register_error_handlers(app)
    """

    @app.errorhandler(AppException)
    def handle_app_exception(e: AppException):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(ValidationError)
    def handle_validation(e: ValidationError):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(e: UnauthorizedError):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(e: ForbiddenError):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(NotFoundError)
    def handle_not_found(e: NotFoundError):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(ConflictError)
    def handle_conflict(e: ConflictError):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(InternalError)
    def handle_internal(e: InternalError):
        _log(app, e)
        return jsonify(e.to_dict()), e.status_code

    # Catch-all for unhandled Python exceptions in production
    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        app.logger.exception("%s%s[500] Unhandled exception — %s%s", _BOLD, _RED, e, _RESET)
        return jsonify({"error": "An unexpected error occurred."}), 500