import re
from werkzeug.security import check_password_hash

from database.models.user import UserRole
from utils.exceptions import ConflictError, ValidationError

def verify_password_match(password: str, hashed_password: str):
    """Verifica una contraseña contra su hash. Lanza ValidationError si no coincide."""
    if not check_password_hash(hashed_password, password):
        raise ValidationError("Contraseña inválida")

def validate_email(email: str):
    """Valida que el email tenga un formato válido. Lanza ValidationError si no es válido."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("Formato de email inválido")

def validate_password(password: str, min_length: int = 8):
    """Valida que la contraseña tenga longitud mínima. Lanza ValidationError si es muy corta."""
    if not password:
        raise ValidationError("La contraseña es requerida")
    if len(password.strip()) < min_length:
        raise ValidationError(f"La contraseña debe tener mínimo {min_length} caracteres")

def validate_daily_salary(daily_salary: float):
    if daily_salary < 0:
        raise ConflictError("El salario diario no puede ser negativo.")