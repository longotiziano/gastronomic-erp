class AppException(Exception):
    """Base exception for all application errors."""
    status_code: int = 500
    message: str = "An unexpected error occurred."

    def __init__(self, message: str = None):
        self.message = message or self.__class__.message
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {"error": self.message}


# ------------------------------------------------------------------ #
#  400 — Bad Request / Validation
# ------------------------------------------------------------------ #

class ValidationError(AppException):
    status_code = 400
    message = "Invalid or missing data."

    def __init__(self, message: str = None, fields: dict = None):
        super().__init__(message)
        self.fields = fields  # Optional: {"email": "is required", "price": "must be positive"}

    def to_dict(self) -> dict:
        payload = {"error": self.message}
        if self.fields:
            payload["fields"] = self.fields
        return payload


# ------------------------------------------------------------------ #
#  401 — Unauthorized
# ------------------------------------------------------------------ #

class UnauthorizedError(AppException):
    status_code = 401
    message = "Authentication required."


# ------------------------------------------------------------------ #
#  403 — Forbidden
# ------------------------------------------------------------------ #

class ForbiddenError(AppException):
    status_code = 403
    message = "You do not have permission to perform this action."


# ------------------------------------------------------------------ #
#  404 — Not Found
# ------------------------------------------------------------------ #

class NotFoundError(AppException):
    status_code = 404
    message = "Resource not found."

    def __init__(self, resource: str = None):
        msg = f"{resource} not found." if resource else self.__class__.message
        super().__init__(msg)


# ------------------------------------------------------------------ #
#  409 — Conflict / Duplicate
# ------------------------------------------------------------------ #

class ConflictError(AppException):
    status_code = 409
    message = "A conflict occurred with the current state of the resource."


# ------------------------------------------------------------------ #
#  500 — Internal Server Error
# ------------------------------------------------------------------ #

class InternalError(AppException):
    status_code = 500
    message = "An unexpected error occurred. Please try again later."