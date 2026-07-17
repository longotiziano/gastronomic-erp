from flask_sqlalchemy.pagination import Pagination
from werkzeug.security import generate_password_hash
from flask import request

from database.models.user import User, UserRole
from database.repositories.users import UserRepository
from seeds.users import validate_daily_salary, validate_email, validate_password, verify_password_match
from seeds.bars import validate_bar_id
from utils.exceptions import ConflictError, NotFoundError, ValidationError
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
    bar_id: int,
    role: UserRole | str = UserRole.waiter,
    address: str | None = None,
    daily_salary: float = 0.0,
) -> User:
    user_repo = UserRepository()
    email = clean_string(email)
    name = clean_string(name, title=True)
    role = clean_string(role) if isinstance(role, str) else role

    if user_repo.get_by_email(email):
        raise ConflictError("El email ya se encuentra registrado.")

    validate_email(email)
    validate_password(password)
    
    if isinstance(role, str):
        if role not in UserRole.__members__:
            raise ConflictError(f"Rol inválido: {role}")
        else:
            role = UserRole[role]

    validate_daily_salary(daily_salary)
    validate_bar_id(bar_id)

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

def update_user(user_id: int, updates: dict) -> None:
    if not updates:
        raise ValidationError("No hay campos para actualizar")

    processed_updates = {}

    if updates.get('name'):
        processed_updates['name'] = clean_string(updates['name'], title=True)

    if updates.get('email'):
        email = clean_string(updates['email'])
        validate_email(email)
        processed_updates['email'] = email

    if updates.get('rol'):
        if isinstance(updates.get('rol'), str):
            role = clean_string(updates['rol'])
            if role not in UserRole.__members__:
                raise ConflictError(f"Rol inválido: {role}")
            else:
                processed_updates['rol'] = UserRole[role]

    if updates.get('password'):
        password = updates['password']
        validate_password(password)
        processed_updates['password'] = generate_password_hash(password)

    if updates.get('daily_salary'):
        validate_daily_salary(updates['daily_salary'])
        processed_updates['daily_salary'] = updates['daily_salary']

    if updates.get('address'):
        processed_updates['address'] = clean_string(updates['address'], title=True)
    
    if updates.get('bar_id'):
        bar_id = updates['bar_id']
        validate_bar_id(bar_id)
        processed_updates['bar_id'] = bar_id

    if not processed_updates:
        raise ValidationError("No hay campos válidos para actualizar")

    user_repository = UserRepository()
    user = user_repository.update(user_id, **processed_updates)
    if user is None:
        raise ConflictError(f"No se ha podido actualizar el usuario con ID {user_id}.")

def alt_user_status(user_id: int) -> User:
    user_repo = UserRepository()
    user = user_repo.get_by_id(user_id)
    if not user:
        raise NotFoundError("Usuario no encontrado.")

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