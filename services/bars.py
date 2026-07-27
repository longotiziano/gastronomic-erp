from services.base_service import BaseCrudService
from database.repositories.bars import BarRepository
from database.models.bar import Bar
from utils.exceptions import NotFoundError

from flask import session

class BarService(BaseCrudService):
    def __init__(self):
        super().__init__(BarRepository())
    
    
    def get_bar_name(self, bar_id: int) -> str:
        "Receives an ID, and returns its name. Raises NotFoundError if it wasn't found."
        bar = self.repo.get_by_id(bar_id)
        if not bar:
            raise NotFoundError(f"No se ha podido encontrar el bar con ID: {bar_id}")
        return bar.name
    
    def get_session_bar(self, bars: list[Bar]) -> int | None:
        """Gets the selected bar_id in the Flask's session.
        In case of not finding any bar_id, then puts a value depending on the user:
        - if the user has `administrator` role, then puts the first bar found in database != 'General'
        - if the user has any other role, looks for the bar_id that the user is associated with.
        Returns None if no valid bar could be resolved."""
        selected_bar_id: int | None = session.get("bar_id")
        user_rol = session.get("user_rol")

        if selected_bar_id and not any(b.id == selected_bar_id for b in bars):
            selected_bar_id = None

        if not selected_bar_id:
            if user_rol == "administrator":
                bar = next((b for b in bars if b.name != "General"), None)
                selected_bar_id = bar.id if bar else None
            else:
                user_bar_id = session.get("user_bar_id")
                bar = next((b for b in bars if b.id == user_bar_id), None)
                selected_bar_id = bar.id if bar else None
                
            session["bar_id"] = selected_bar_id
            session["bar_name"] = bar.name if bar else None

        return selected_bar_id