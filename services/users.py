from werkzeug.security import generate_password_hash

from database.models.user import User, UserRole
from database.repositories.users import UserRepository
from seeds.users import validate_email, validate_password, verify_password_match
from utils.exceptions import ConflictError
from utils.helpers import clean_string


def hash_password(password: str) -> str:
    """Hashea una contraseña usando Werkzeug."""
    return generate_password_hash(password)


def create_user(
    name: str,
    email: str,
    password: str,
    role: UserRole | str = UserRole.waiter,
    bar_id: int | None = None,
    address: str | None = None,
    daily_salary: float = 0.0,
) -> User:
    user_repo = UserRepository()
    email = clean_string(email)
    name = clean_string(name, title=True)
    if user_repo.get_by_email(email):
        raise ConflictError("El email ya se encuentra registrado.")

    validate_email(email)
    validate_password(password)

    if isinstance(role, str):
        role = UserRole[role] if role in UserRole.__members__ else UserRole.waiter

    hashed_password = hash_password(password)
    user = user_repo.create(
        name=name,
        email=email,
        password=hashed_password,
        rol=role,
        bar_id=bar_id,
        address=address,
        daily_salary=daily_salary,
    )
    return user


def login_user(email: str, password: str) -> User:
    user_repo = UserRepository()
    email = clean_string(email)
    user = user_repo.get_active_by_email(email)
    if not user:
        raise ConflictError("Usuario no encontrado o inactivo.")

    verify_password_match(password, user.password)
    return user