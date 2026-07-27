from flask import Blueprint, render_template, g, redirect, url_for, request
from utils.helpers import is_admin
from utils.auth_decorator import require_bar
from services.sales import SaleService
from services.bars import BarService
from utils.exceptions import ValidationError

sales_bp = Blueprint("sales", __name__)

sales_service = SaleService()
bs = BarService()

@sales_bp.route("/sales")
@require_bar
def render_sales():
    return render_template("sections/sales.html",
        selected_bar_id = g.bar_id,
        bar_selection = g.bars,
        is_admin=is_admin()
    )
    
@sales_bp.post("/sales/upload_file")
@require_bar
def upload_file():
    print("Entrando a la carga de archivos")
    file = request.files.get("file")
    if not file:
        raise ValidationError("No se ha proporcionado un archivo válido.")
    
    return redirect(url_for("sales.render_sales"))
