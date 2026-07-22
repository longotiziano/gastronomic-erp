from database.models.user import User
from database.repositories.users import UserRepository
from services.base_service import BaseCrudService
from utils.exceptions import ValidationError
from validators.users import validate_email, verify_password_match
from werkzeug.security import generate_password_hash
from utils.helpers import clean_string

class UserService(BaseCrudService):
    repo: UserRepository
    
    
    def __init__(self):
        super().__init__(UserRepository())


    def _generate_password_hash(self, password: str) -> str:
            if len(password) >= 8:
                return generate_password_hash(password)
            else:
                raise ValidationError("La contraseña debe tener al menos 8 caracteres.")


    def create(self, **data) -> User:
        if data.get("confirm_password"):
            del data["confirm_password"]
            
        email = data.get("email")
        password = data.get("password")
        if email and password:
            email = clean_string(email)
            validate_email(email)
            data["password"] = self._generate_password_hash(password)

        return super().create(**data)
    

    def update(self, entity_id: int, data: dict) -> User:
        if data.get("confirm_password"):
            del data["confirm_password"]
        
        email = data.get("email")
        password = data.get("password")
        if email:
            email = clean_string(email)
            validate_email(email)
        if password:
            data["password"] = self._generate_password_hash(password)
            
        return super().update(entity_id, data)
    
    
    def login(self, email: str, password: str) -> User:
        email = clean_string(email)
        validate_email(email)
        user = self.repo.get_by_email(email)
        if not user:
            raise ValidationError("Usuario no encontrado.")
        
        verify_password_match(password, user.password)
        return user