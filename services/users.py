from database.repositories.employee import EmployeeRepository
from database.repositories.users import UserRepository
from services.base import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__(UserRepository(), check_existence="email")

    def get_active_by_email(self, email: str):
        return self.repository.get_active_by_email(email)
    
    def verify_credentials(self, email: str, password: str):
        return self.repository.verify_credentials(email, password)


class EmployeeService(BaseService):
    def __init__(self):
        super().__init__(EmployeeRepository(), check_existence="user_id")

    def get_by_bar(self, bar_id: int, active_only: bool = True):
        return self.repository.get_by_bar(bar_id, active_only=active_only)

    def get_by_role(self, rol, bar_id: int | None = None):
        return self.repository.get_by_role(rol, bar_id=bar_id)

    def get_by_user(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def fire(self, id: int):
        return self.repository.fire(id)