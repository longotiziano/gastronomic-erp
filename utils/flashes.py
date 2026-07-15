from flask import flash
import json
from typing import Literal

def flash_message(
        title: str, 
        description: str = '', 
        category: Literal['error', 'success', 'warning', 'info'] = 'error'
    ) -> None:
    """
    Flashea un mensaje con un formato específico para ser mostrado con SweetAlert en el frontend.
    El mensaje se formatea como un JSON con las claves "title" y "text", y se categoriza con la categoría dada (por defecto, 'error').
    """
    flash(json.dumps({
        "title": title,
        "text": description
    }), category)