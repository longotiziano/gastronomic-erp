from flask import Blueprint, render_template, g, redirect, url_for, request
from werkzeug.datastructures import FileStorage

from utils.helpers import is_admin
from utils.auth_decorator import require_bar
from services.sales import SaleService
from services.bars import BarService
from validators.extras.excel_validator import validate_excel_file

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
    file: FileStorage | None = request.files.get("file")
    validate_excel_file(file)
    
    ok, table = sales_service.file_processor(file)
    if not ok:
        print("Hay productos faltantes. Procediendo con el renderizado de la tabla")
        return render_template("sections/sales.html",
            missing_table = table,
            selected_bar_id = g.bar_id,
            bar_selection = g.bars,
            is_modal = True,
            is_admin = is_admin()
        )
    
    return redirect(url_for("sales.render_sales"))
