from datetime import date
from datetime import datetime

from urllib.parse import urlparse, urljoin
from flask import request, url_for

def clean_string(input_string: str, title=False) -> str:
    input_string = input_string.strip()
    return input_string.title() if title else input_string.lower()

def format_date(date_obj: date) -> str:
    if date_obj is None:
        return "N/A"
    return date_obj.strftime("%d-%m-%Y")

def is_admin() -> bool:
    from flask import session
    return session.get("user_rol") == "administrator"
    
def _get_saludo() -> str:
    hora = datetime.now().hour
    if hora < 12:
        return "Buenos días"
    if hora < 20:
        return "Buenas tardes"
    return "Buenas noches"

def _get_safe_next() -> str:
    """
    Devuelve la URL a la que hay que volver después de cambiar de bar:
    prioriza el campo oculto 'next' del form, y si no vino usa el
    Referer. Si ninguno es una URL del propio sitio, cae al index
    (nunca redirige a un dominio externo).
    """
    candidate = request.form.get("next") or request.referrer
 
    if candidate:
        site = urlparse(request.host_url)
        target = urlparse(urljoin(request.host_url, candidate))
        if target.scheme in ("http", "https") and target.netloc == site.netloc:
            return candidate
 
    return url_for("main.index")