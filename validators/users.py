import re
from werkzeug.security import check_password_hash

from utils.exceptions import ValidationError

def verify_password_match(password: str, hashed_password: str):
    """Verifica una contraseña contra su hash. Lanza ValidationError si no coincide."""
    if not check_password_hash(hashed_password, password):
        raise ValidationError("Contraseña inválida")

def validate_email(email: str):
    """Valida que el email tenga un formato válido. Lanza ValidationError si no es válido."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError("Formato de email inválido")