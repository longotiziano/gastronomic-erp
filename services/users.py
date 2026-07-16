from flask_sqlalchemy.pagination import Pagination
from werkzeug.security import generate_password_hash
from flask import request

from database.models.user import User, UserRole
from database.repositories.users import UserRepository
from seeds.users import validate_email, validate_password, verify_password_match
from utils.exceptions import ConflictError
from utils.helpers import clean_string

def obtain_users() -> Pagination:
    user_repo = UserRepository()
    page = request.args.get("page", 1, type=int)
    pagination = user_repo.paginate(page=page, per_page=20, active_only=False)
    return pagination

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
        if role not in UserRole.__members__:
            raise ConflictError(f"Rol inválido: {role}")
        else:
            role = UserRole[role]

    hashed_password = generate_password_hash(password)
    user = user_repo.create(
        name=name,
        email=email,
        password=hashed_password,
        rol=role,
        bar_id=bar_id,
        address=address,
        daily_salary=daily_salary,
    )
    if not user:
        raise ConflictError("No se pudo crear el usuario.")

    return user

def alt_user_status(user_id: int) -> User:
    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)
    if not user:
        raise ConflictError("Usuario no encontrado.")

    user.record_status = not user.record_status
    updated_user = user_repo.update(user_id, record_status=user.record_status)
    if not updated_user:
        raise ConflictError("No se pudo actualizar el estado del usuario.")

    return updated_user

def login_user(email: str, password: str) -> User:
    user_repo = UserRepository()
    email = clean_string(email)
    user = user_repo.get_active_by_email(email)
    if not user:
        raise ConflictError("Usuario no encontrado o inactivo.")

    verify_password_match(password, user.password)
    return user