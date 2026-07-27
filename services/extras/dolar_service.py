"""
Servicio para obtener la cotización del dólar.
Encapsula la llamada externa y un cache simple para no pegarle
a la API en cada request del index.
"""
 
import time
import requests
 
DOLAR_API_URL = "https://dolarapi.com/v1/dolares"
CACHE_TTL_SECONDS = 60 * 60  # 1 hora
 
# Cache en memoria del proceso. Si corrés con múltiples workers (gunicorn, etc.)
# cada uno va a tener su propio cache, lo cual está bien para este caso de uso.
_cache = {
    "data": None,
    "timestamp": 0,
}
 
 
def get_cotizaciones_dolar() -> dict:
    """
    Devuelve un dict indexado por casa de cambio, ej:
    {
        "oficial": {"compra": 1230.0, "venta": 1250.0},
        "blue":    {"compra": 1280.0, "venta": 1300.0},
        ...
    }
    Usa cache de 1 hora. Si la API falla, devuelve el último dato
    cacheado (aunque esté vencido) o un dict vacío si nunca hubo dato.
    """
    now = time.time()
 
    if _cache["data"] is not None and (now - _cache["timestamp"]) < CACHE_TTL_SECONDS:
        return _cache["data"]
 
    try:
        response = requests.get(DOLAR_API_URL, timeout=5)
        response.raise_for_status()
        raw = response.json()
 
        cotizaciones = {
            item["casa"]: {
                "compra": item.get("compra"),
                "venta": item.get("venta"),
            }
            for item in raw
        }
 
        _cache["data"] = cotizaciones
        _cache["timestamp"] = now
        return cotizaciones
 
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"[dolar_service] Error al obtener cotización: {e}")
        # Si hay algo cacheado (aunque vencido), es mejor mostrar eso que nada.
        return _cache["data"] or {}
 
 
def invalidar_cache():
    """Útil para forzar un refresh manual desde un endpoint admin, si hiciera falta."""
    _cache["data"] = None
    _cache["timestamp"] = 0