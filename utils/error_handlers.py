import traceback
from flask import Flask, flash, redirect, request, url_for
from utils.exceptions import AppException

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

    @app.errorhandler(AppException)
    def handle_app_exception(e: AppException):
        _log(app, e)
        flash(e.message, "danger")
        return redirect(request.referrer or url_for("main.index"))

    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        app.logger.exception("%s%s[500] Unhandled exception — %s%s", _BOLD, _RED, e, _RESET)
        flash("Ocurrió un error inesperado.", "danger")
        return redirect(request.referrer or url_for("main.index"))